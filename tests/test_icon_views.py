# from django.test import TestCase
from wagtail.tests.utils import WagtailTestUtils
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from wagtail_icons.models import (
    Group,
    Icon
)
import os
from django.core.files import File
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class TestIconViews(WagtailTestUtils, TestCase):

    def setUp(self):
        """Create Timeline page and two event pages"""
        # create new superuser
        self.superuser = User.objects.create_superuser(username='superuser', email='superuser@gmail.com')
        self.superuser.set_password('superuser123')
        self.superuser.save()
        # login superuser
        self.logged_in_superuser = Client()
        self.logged_in_superuser.login(username='superuser', password='superuser123')

        # create new regular user
        self.user = User.objects.create(username='user')
        self.user.set_password('user123')
        self.user.save()
        # login regular user
        self.logged_in_user = Client()
        self.logged_in_user.login(username='user', password='user123')

        # create group
        group = Group.objects.create(
            title = "Group 1",
            slug = "group_1"
        )

        fixtures_path = os.path.join(os.getcwd(), 'icons/tests/fixtures')
        fixtures = os.listdir(fixtures_path)
        count = 0
        for icon_title in fixtures:
            if count <= 5:
                icon = Icon(title=icon_title.split('.')[0])
                with open(os.path.join(fixtures_path, icon_title), 'rb') as icon_file:
                    icon.file.save(icon_title, File(icon_file), save=True)
                icon.save()
            else:
                break
            count += 1
        group.icons.add(Icon.objects.get(id=1), Icon.objects.get(id=2))




    def test_icons_index_view(self):
        response = self.logged_in_user.get(reverse('wagtailicons:index'))
        self.assertEqual(response.status_code, 302)
        response = self.logged_in_superuser.get(reverse('wagtailicons:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], None)
        context_icons = [icon.id for icon in response.context['icons'].object_list]
        self.assertEqual(list(Icon.objects.all().order_by('-created_at').values_list('id', flat=True)), context_icons)
        response = self.logged_in_superuser.get(reverse('wagtailicons:index'), {'group':Group.objects.get(slug='group_1').id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], Group.objects.get(slug='group_1'))
        context_icons = [icon.id for icon in response.context['icons'].object_list]
        self.assertEqual(list(Group.objects.get(slug='group_1').icons.all().order_by('-created_at').values_list('id', flat=True)), context_icons)

    def test_icons_add_view(self):
        response = self.logged_in_user.get(reverse('wagtailicons:add'))
        self.assertEqual(response.status_code, 302)
        response = self.logged_in_superuser.get(reverse('wagtailicons:add'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], None)
        response = self.logged_in_superuser.get(reverse('wagtailicons:add'), {'group':Group.objects.get(slug='group_1').id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], Group.objects.get(slug='group_1'))
        context_icons = [icon.id for icon in response.context['icons'].object_list]
        non_group_icons = [icon.id for icon in Icon.objects.all() if icon.id not in response.context['group'].icons.all().values_list('id', flat=True)]
        self.assertEqual(non_group_icons, context_icons)


    # def test_icons_edit_view(self):
    #     self.fail('to do')

    def test_can_delete_icon(self):
        # delete from all icons list
        icons_num = Icon.objects.all().count()
        delete_icon = Icon.objects.first()
        delete_icon_id = delete_icon.id
        response = self.logged_in_superuser.post(reverse('wagtailicons:add'),  data={'action':'delete', 'icon_id':delete_icon.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Icon.objects.all().count(), icons_num - 1)
        self.assertNotIn(delete_icon_id, Icon.objects.all().values_list('id', flat=True))
        # delete from specific groups 
        group = Group.objects.first()
        delete_icon = Icon.objects.first()
        response = self.logged_in_superuser.post(reverse('wagtailicons:index'),  data={'type':'delete', 'icons':[delete_icon.id], 'group':group.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Icon.objects.all().count(), icons_num-1)
        self.assertNotIn(delete_icon.id, group.icons.all().values_list('id', flat=True))
        
    def test_search_icon(self):
        search_query = 'alarm'
        matching_icons = Icon.objects.filter(title__icontains=search_query.lower()).values_list('id', flat=True)
        response = self.logged_in_superuser.get(reverse('wagtailicons:index'), data={'q':search_query})
        self.assertEqual(response.status_code, 200)
        context_icons = [icon.id for icon in response.context['icons'].object_list]
        self.assertEqual(list(matching_icons), context_icons)

    def test_can_add_icon(self):
        # test add existing icon to group
        group = Group.objects.first()
        add_icon = [icon for icon in Icon.objects.all() if icon not in group.icons.all()][0]
        response = self.logged_in_superuser.post(reverse('wagtailicons:add'), data={'type':'add_existing', 'group': group.id, 'icons':add_icon.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(add_icon.id, group.icons.all().values_list('id', flat=True))
        # test can upload new icon
        icons_count = Icon.objects.all().count()
        upload_icon_path = os.path.join(os.getcwd(), 'icons/tests/fixtures/bar-chart-line-fill.svg')
        with open(upload_icon_path, 'rb') as icon_file:
            upload_icon = SimpleUploadedFile('bar-chart-line-fill.svg', icon_file.read(), 'image/svg+xml')
        response = self.logged_in_superuser.post(reverse('wagtailicons:add'), data={'action':'upload', 'icons':[upload_icon], 'urls':['icon_url']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Icon.objects.all().count(), icons_count+1)
        self.assertIn('bar-chart-line-fill', Icon.objects.all().values_list('title', flat=True))


    def test_can_update_icon(self):
        update_icon = Icon.objects.get(title='badge-8k-fill')
        update_icon_id = update_icon.id
        response = self.logged_in_superuser.post(reverse('wagtailicons:edit'), data={'type':'update', 'icon_id':update_icon_id, 'title': 'New Title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Icon.objects.get(id=update_icon_id).title, 'New Title')
