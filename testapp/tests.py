import datetime

from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from .models import ClassSubject, Post ,Profile, Thread, Message
from django.contrib.auth.models import User

# Create your tests here.

def create_post(post_title, post_text, pub_date, book_ISBN, associated_dept, course_id):
    """
    Create a post given various parameters. Note that favorite cannot be added during post creation (must be added separately)
    """
    return Post.objects.create(post_title=post_title, post_text=post_text, pub_date=pub_date, book_ISBN=book_ISBN, associated_dept=associated_dept, course_id=course_id)

def create_test_user(username, password):
    return User.objects.create_user(username=username, password=password)

class IndexViewTests(TestCase):
    def setUp(self):
        """
        Create the user to be used for the tests
        """
        self.user = create_test_user(username="testCaseUser1", password="testCasePass1")
        self.client.login(username="testCaseUser1", password="testCasePass1")

    def test_no_posts(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('testapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_post(self):
        """
        Check general post creation and display
        """
        testpost = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        response = self.client.get(reverse('testapp:index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            [testpost],
        )

    def valid_dates_on_posts(self):
        """
        Make sure all posts have valid dates
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_multiple_posts(self):
        """
        Check that multiple posts are properly displayed
        """
        testpost1 = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        testpost2 = create_post(post_title="CS 4102 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        response = self.client.get(reverse('testapp:index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            [testpost1, testpost2],
            ordered=False
        )
    
    def tearDown(self):
        """
        Delete the user created for this test
        """
        self.user.delete()

class FavoritesViewTest(TestCase):
    def setUp(self):
        """
        Create the user to be used for the tests
        """
        self.user = create_test_user(username="testCaseUser1", password="testCasePass1")
        self.client.login(username="testCaseUser1", password="testCasePass1")

    def test_no_favorites(self):
        """
        If no posts are favorited, then no posts are displayed
        """
        response = self.client.get(reverse('testapp:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_favorite(self):
        """
        Check that favorites shows up
        """
        testfav1 = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        testfav1.favorite.add(self.user)
        response = self.client.get(reverse('testapp:favorites'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            [testfav1],
            ordered=False
        )

    def test_multiple_favorites(self):
        """
        Check that multiple favorites show up
        """
        testfav1 = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        testfav2 = create_post(post_title="CS 4102 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='4102')
        testfav1.favorite.add(self.user)
        testfav2.favorite.add(self.user)
        response = self.client.get(reverse('testapp:favorites'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            [testfav1, testfav2],
            ordered=False
        )

    def test_favorite_from_index(self):
        """
        Check that favoriting from index page works
        """
        # First create a post, favorite it
        testfav1 = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        response = self.client.post(reverse('testapp:favorite_post', kwargs={'fav_id': testfav1.id}))
        self.assertRedirects(response, reverse('testapp:index'), status_code=302, target_status_code=200)

        # Then make another get request to favorites page to check it
        response = self.client.get(reverse('testapp:favorites'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            [testfav1],
            ordered=False
        )

    def test_unfavorite_from_index(self):
        """
        Check that unfavoriting from index page works
        """
        # First create a post, favorite it, and then unfavorite it
        testfav1 = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        testfav1.favorite.add(self.user)
        response = self.client.post(reverse('testapp:remove_favorite', kwargs={'fav_id': testfav1.id}))
        self.assertRedirects(response, reverse('testapp:index'), status_code=302, target_status_code=200)

        # Then make another get request to favorites page to check it
        response = self.client.get(reverse('testapp:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_unfavorite_from_fav(self):
        """
        Check that unfavoriting from favorites page works
        """
        # First create a post, favorite it, and then unfavorite it
        testfav1 = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        testfav1.favorite.add(self.user)
        response = self.client.post(reverse('testapp:remove_favorite_from_fav', kwargs={'fav_id': testfav1.id}))
        self.assertRedirects(response, reverse('testapp:favorites'), status_code=302, target_status_code=200)

        # Then make another get request to favorites page to check it
        response = self.client.get(reverse('testapp:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def tearDown(self):
        """
        Delete the user created for this test
        """
        self.user.delete()

class ThreadListViewTest(TestCase):
    def setUp(self):
        """
        Create the user to be used for the tests
        """
        self.user1 = create_test_user(username="testCaseUser1", password="testCasePass1")
        self.user2 = create_test_user(username="testCaseUser2", password="testCasePass2")
        self.client.login(username="testCaseUser1", password="testCasePass1")

    def test_create_thread(self):
        testthread = Thread.objects.create(user1=self.user1, user2=self.user2, subject_text="CS 4102 Textbook!")
        response = self.client.get(reverse('testapp:threads'))
        self.assertQuerysetEqual(
            response.context['thread_list'],
            [testthread],
        )

    def test_multiple_threads(self):
        testthread1 = Thread.objects.create(user1=self.user1, user2=self.user2, subject_text="CS 4102 Textbook!")
        testthread2 = Thread.objects.create(user1=self.user1, user2=self.user2, subject_text="CS 3102 Textbook!")
        response = self.client.get(reverse('testapp:threads'))
        self.assertQuerysetEqual(
            response.context['thread_list'],
            [testthread1, testthread2],
            ordered=False
        )

    def tearDown(self):
        """
        Delete the user created for this test
        """
        self.user1.delete()
        self.user2.delete()

class ThreadViewTest(TestCase):
    def setUp(self):
        """
        Create the user to be used for the tests
        """
        self.user1 = create_test_user(username="testCaseUser1", password="testCasePass1")
        self.user2 = create_test_user(username="testCaseUser2", password="testCasePass2")
        self.thread = Thread.objects.create(user1=self.user1, user2=self.user2, subject_text="CS 4102 Textbook!")
        self.client.login(username="testCaseUser1", password="testCasePass1")

    def test_create_message(self):
        testmessage = Message.objects.create(thread=self.thread,sender=self.user1,receiver=self.user2,message_text="Hi! Are you selling a textbook?")
        response = self.client.get(reverse('testapp:thread_view', kwargs={'pk': self.thread.id}))
        self.assertQuerysetEqual(
            response.context['message_list'],
            [testmessage],
        )

    def test_multiple_messages(self):
        testmessage1 = Message.objects.create(thread=self.thread,sender=self.user1,receiver=self.user2,message_text="Hi! Are you selling a textbook?")
        testmessage2 = Message.objects.create(thread=self.thread,sender=self.user2,receiver=self.user1,message_text="Yes! I am selling it for $20, does that sound good?")
        response = self.client.get(reverse('testapp:thread_view', kwargs={'pk': self.thread.id}))
        self.assertQuerysetEqual(
            response.context['message_list'],
            [testmessage1, testmessage2],
            ordered=False
        )

    def tearDown(self):
        """
        Delete the user created for this test
        """
        self.user1.delete()
        self.user2.delete()
        self.thread.delete()

class ClassSubjectTest(TestCase):
    def setUp(self):
        """
        Create the user to be used for the tests
        """
        self.user = create_test_user(username="testCaseUser1", password="testCasePass1")
        self.client.login(username="testCaseUser1", password="testCasePass1")

    def test_class_subject(self):
        """
        Check that page redirects properly on class search
        """
        form_data = {'class_subject': 'CS'}
        response = self.client.post(reverse('testapp:classsubject'), form_data)
        self.assertRedirects(response, reverse('testapp:course'), status_code=302, target_status_code=200)

    def tearDown(self):
        """
        Delete the user created for this test
        """
        self.user.delete()

    def test_invalid_dept(self):
        """
        If no class subject matches the input, an appropriate message is displayed.
        """
        form_data = {'class_subject': 'CD'}
        response = self.client.post(reverse('testapp:classsubject'), form_data)
        self.assertRedirects(response, "/testapp/course", status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        response = self.client.post(reverse('testapp:classsubject'), form_data, follow=True)
        self.assertContains(response, "That department pneumonic does not exist.")

class SearchTests(TestCase):
    def setUp(self):
        """
        Create the user to be used for the tests
        """
        self.user = create_test_user(username="testCaseUser1", password="testCasePass1")
        self.post = create_post(post_title="CS 3240 Textbook", post_text="Selling a used textbook in good condition!", pub_date="10/24/22", book_ISBN='9783161484100', associated_dept='CS', course_id='3330')
        self.client.login(username="testCaseUser1", password="testCasePass1")

    def test_search_allows_input(self):
        """
        Check that search bar reads input and redirects properly
        """
        #form_data = {"q": "CS"}
        response = self.client.get("/testapp/post_search?q=CS")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            [self.post],
        )

    def test_empty_search(self):
        """
        If there was no search
        """
        #form_data = {"q": ""}
        response = self.client.get("/testapp/post_search?q=")
        # self.assertRedirects(response, "/testapp/post_search?q=CS", status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # response = self.client.get(reverse('testapp:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available")
        self.assertEqual(response.context['post_list'], None)

    def test_bad_search(self):
        """
        If there was a search that returned no posts
        """
        #form_data = {"q": "potatopotahtoxyz"}
        response = self.client.get("/testapp/post_search?q=")
        # self.assertRedirects(response, "/testapp/post_search?q=CS", status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # response = self.client.get(reverse('testapp:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available")
        self.assertEqual(response.context['post_list'], None)

    def tearDown(self):
        """
        Delete the user created for this test
        """
        self.user.delete()
        self.post.delete()