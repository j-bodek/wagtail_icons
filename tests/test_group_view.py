# from django.test import TestCase
from wagtail.tests.utils import WagtailTestUtils
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from wagtail_icons.models import (
    Group
)
from django.urls import reverse

class TestGroupViews(WagtailTestUtils, TestCase):

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

        # create empty group
        empty_group = Group.objects.create(
            title = "Empty Group",
            slug = "empty_group"
        )


    def test_group_index_status_code(self):
        response = self.logged_in_user.get(reverse('wagtailicons:groups'))
        self.assertEqual(response.status_code, 302)
        response = self.logged_in_superuser.get(reverse('wagtailicons:groups'))
        self.assertEqual(response.status_code, 200)

    def test_group_add_view_status_code(self):
        response = self.logged_in_superuser.get(reverse('wagtailicons:add_group'))
        self.assertEqual(response.status_code, 200)
        response = self.logged_in_user.get(reverse('wagtailicons:add_group'))
        self.assertEqual(response.status_code, 302)
    
    def test_can_add_group(self):
        group_num = Group.objects.all().count()
        response = self.logged_in_superuser.post(reverse('wagtailicons:add_group'), data={'title':'New Group', 'slug':'new_group'})
        self.assertRedirects(response, reverse('wagtailicons:groups'), 302)
        self.assertIn('New Group', Group.objects.all().values_list('title', flat=True))
        self.assertIn('new_group', Group.objects.all().values_list('slug', flat=True))
        self.assertEqual(group_num+1, Group.objects.all().count())

    def test_can_delete_group(self):
        group_num = Group.objects.all().count()
        delete_group = Group.objects.first()
        delete_group_title, delete_group_slug = delete_group.title, delete_group.slug
        response = self.logged_in_superuser.post(reverse('wagtailicons:groups'), data={'type':'delete', 'groups':[delete_group.id]})
        context_groups = response.context['groups'].object_list
        self.assertNotIn(delete_group_title, context_groups.values_list('title', flat=True))
        self.assertNotIn(delete_group_slug, context_groups.values_list('slug', flat=True))
        self.assertEqual(group_num-1, context_groups.count())

    def test_can_search_groups(self):
        query = 'Empty'
        response = self.logged_in_superuser.get(reverse('wagtailicons:groups'), {'q':query})
        context_groups = response.context['groups'].object_list
        self.assertIn(Group.objects.get(title__icontains=query.lower()), context_groups)

    def test_can_order_groups(self):
        Group.objects.create(
            title='New Group',
            slug='new_group'
        )
        response = self.logged_in_superuser.get(reverse('wagtailicons:groups'), {'ordering':'title'})
        context_groups = response.context['groups'].object_list
        self.assertEqual(list(Group.objects.all().order_by('title').values_list('id', flat=True)), [group.id for group in context_groups])

    def test_group_index_pagination(self):
        for i in range(1, 50):
            Group.objects.create(
                title=f'New Group {str(i)}',
                slug=f'new_group_{str(i)}'
            )
        first_fiveteen_groups = list(Group.objects.all().order_by('-edited').values_list('id', flat=True)[:15])
        response = self.logged_in_superuser.get(reverse('wagtailicons:groups'))
        context_groups = [group.id for group in response.context['groups'].object_list]
        self.assertEqual(first_fiveteen_groups, context_groups)
