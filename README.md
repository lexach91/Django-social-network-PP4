# Social network

## About
This web application is a social network for people who want to share their knowledge and experiences with others and at the same time keep in touch with the people who are interested in the same things.
The application allows to communicate with other users by messages, posting, commenting, and reacting to their posts and comments.

## User Experience Design

### Strategy
Developed for the purpose to make the communication free and easy. The main goal of the application is to make the user experience as pleasant as possible and prolong the user's time on the site.

### Target Audience
People who cannot stand the complexity of modern social media apps and want to have a simple and easy-to-use interface.

### User Stories

#### First Time Visitor Goals
- As a First Time Visitor, I want to be able to easily understand the main purpose of the app, so that I can learn more about this app.
- As a First Time Visitor, I want to be able to easily navigate through the app, so that I can find presented content.
- As a First Time Visitor, I want to be able to register my account, so that I can learn the benefits of the app as a user.
- As a First Time Visitor, I want to be able to find the app useful, so that I can use it according to my needs.

#### Frequent Visitor Goals
- As a Frequent User, I want to be able to log in to my account, so that I can have a personal account.
- As a Frequent User, I want to be able to easily navigate through the app, so that I can find the content without additional efforts.
- As a Frequent User, I want to be able to easily log in and log out, so that I can access my personal account information.
- As a Frequent User, I want to be able to easily recover my password in case I forget it, so that I can recover access to my account.
- As a Frequent User, I can be able to change my password, so that I can be sure that nobody else can access my account.
- As a Frequent User, I want to be able to update my personal data, so that I can keep my account up to date.
- As a Frequent User, I want to be able to update my avatar, so that I can keep my avatar up to date.
- As a Frequent User, I want to be able to delete my profile, so that I can remove my account from the app.
- As a Frequent User, I want to be able to add friends, so that I can communicate with my friends.
- As a Frequent User, I want to be able to delete friends, so that I can feel safe in this social network.
- **As a Frequent User, I want to be able to see whether users are online, so that I can know who is online.**
- As a Frequent User, I want to be able to search through the users of the social network, so that I can find people who I am interested in.
- As a Frequent User, I want to be able to search people by their names, so that I can find people who I know.
- As a Frequent User, I want to be able to add a new post on my page or my friends' pages, so that I can share my knowledge and experiences with others.
- As a Frequent User, I want to be able to add a new comment on my post, so that I can share my knowledge and experiences with others.
- As a Frequent User, I want to be able to add a new comment to other people's post, so that I can share my knowledge and experiences with others.
- As a Frequent User, I want to be able to react to my post, so that I can share my knowledge and experiences with others.
- As a Frequent User, I want to be able to react to other people's post, so that I can share my knowledge and experiences with others.
- As a Frequent User, I want to be able to be able to edit/delete my posts, so that I can change my knowledge and experiences.
- As a Frequent User, I want to be able to create a community, so that I can share my ideas and interests with others.
- As a Frequent User, I want to be able to join a community, so that I can be a part of that community.
- As a Frequent User, I want to be able to add a new post in a community, so that I can share my ideas and interests with others.
- As a Frequent User, I want to be able to add a new comment on my community post, so that I can share my ideas and interests with others.
- As a Frequent User, I want to be able to share my experiences with other users, so that I can share my knowledge and experiences with others.
- As a Frequent User, I want to be able to send messages to other users, so that I can communicate with them.
- As a Frequent User, I want to be able to delete communities that I created, so that I can remove my community from the app.

## Technologies used
- ### Languages:
    + [Python](https://www.python.org/downloads/release/python-385/): the primary language used to develop the server-side of the website.
    + [JS](https://www.javascript.com/): the primary language used to develop interactive components of the website.
    + [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML): the markup language used to create the website.
    + [CSS](https://developer.mozilla.org/en-US/docs/Web/css): the styling language used to style the website.
- ### Frameworks and libraries:
    + [Django](https://www.djangoproject.com/): python framework used to create all the backend logic of the website.
    + [jQuery](https://jquery.com/): was used to control click events and sending AJAX requests.
    + [jQuery User Interface](https://jqueryui.com/) was used to create interactive elements and animations.
    + [Django Channels](https://channels.readthedocs.io/en/latest/): was used to create real-time communication between users.
- ### Databases:
    + [SQLite](https://www.sqlite.org/): was used as a database during the development stage of the website.
    + [PostgreSQL](https://www.postgresql.org/): the database used to store all the data.
- ### Other tools:
    + [Git](https://git-scm.com/): the version control system used to manage the code.
    + [Pip3](https://pypi.org/project/pip/): the package manager used to install the dependencies.
    + [Daphne](https://daphne.readthedocs.io/en/latest/): the webserver used to run the website.
    + [Cloudinary](https://cloudinary.com/): the image hosting service used to upload images and other media.
    + [Psycopg2](https://www.python.org/dev/peps/pep-0249/): the database driver used to connect to the database.
    + [Django-allauth](https://django-allauth.readthedocs.io/en/latest/): the authentication library used to create the user accounts.
    + [Heroku](https://dashboard.heroku.com/): the hosting service used to host the website.
    + [GitHub](https://github.com/): used to host the website's source code.
    + [VSCode](https://code.visualstudio.com/): the IDE used to develop the website.
    + [Chrome DevTools](https://developer.chrome.com/docs/devtools/open/): was used to debug the website.
    + [Font Awesome](https://fontawesome.com/): was used to create the icons used in the website.
    + [Coolors](https://coolors.co/202a3c-1c2431-181f2a-0b1523-65e2d9-925cef-6b28e0-ffffff-eeeeee) was used to make a color palette for the website.
    + [BGJar](https://www.bgjar.com/): was used to make a background images for the website.
    + [W3C Validator](https://validator.w3.org/): was used to validate HTML5 code for the website.
    + [W3C CSS validator](https://jigsaw.w3.org/css-validator/): was used to validate CSS code for the website.
    + [JShint](https://jshint.com/): was used to validate JS code for the website.
    + [PEP8](https://pep8.org/): was used to validate Python code for the website.








---

## Information Architecture

### Database

* During the earliest stages of the project, the database was created using SQLite.
* The database was then migrated to PostgreSQL.



### Data Modeling

1. **Allauth User Model**
    - The user model was created using [Django-allauth](https://django-allauth.readthedocs.io/en/latest/).
    - The user model was then migrated to PostgreSQL.

2. **Profile Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| User          | user          | OneToOneField | User, on_delete=models.CASCADE, related_name='profile'    |
| Avatar        | avatar        | CloudinaryField    | folder='avatars', null=True, blank=True      |
| Birthday      | birth_date    | DateField    | null=True, blank=True      |
| First Name    | first_name    | CharField    | max_length=50, null=True, blank=True      |
| Last Name     | last_name     | CharField    | max_length=50, null=True, blank=True      |
| friends       | friends       | ManyToManyField | to=User, related_name='friends', blank=True      |
| Country       | country       | CharField    | max_length=50, null=True, blank=True      |
| City          | city          | CharField    | max_length=50, null=True, blank=True      |
| Bio           | bio           | TextField    | max_length=500, null=True, blank=True      |

3. **Community Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Name          | name          | CharField    | max_length=25, unique=True, blank=False    |
| Slug          | slug          | SlugField    | unique=True, blank=False    |
| Description   | description   | TextField    | max_length=200, blank=True    |
| BG Image      | bg_image      | CloudinaryField    | folder='community_bg_images', null=True, blank=True    |
| Logo          | logo          | CloudinaryField    | folder='community_logos', null=True, blank=True    |
| Members       | members       | ManyToManyField | to=User, related_name='communities', blank=True    |
| Creator       | creator       | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='created_communities'    |
| Created On    | created_on    | DateTimeField | auto_now_add=True    |
| Updated On    | updated_on    | DateTimeField | auto_now=True    |

4. **Chat Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Members       | members       | ManyToManyField | to=User, related_name='chats', blank=True    |
| Created at    | created_at    | DateTimeField | auto_now_add=True    |
| Last message  | last_message_at  | DateTimeField | auto_now=True    |

5. **Message Model**


| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Chat          | chat          | ForeignKey    | to=Chat, on_delete=models.CASCADE, related_name='messages'    |
| Author        | author        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='messages'    |
| Content       | content       | TextField    | max_length=500, null=True, blank=True      |
| Has Media     | has_media     | BooleanField | default=False      |
| Is Read       | is_read       | BooleanField | default=False      |
| Image         | image         | CloudinaryField    | folder='messages', null=True, blank=True    |
| Video         | video         | CloudinaryField    | folder='messages', null=True, blank=True    |
| Created at    | created_at    | DateTimeField | auto_now_add=True    |
| Updated at    | updated_at    | DateTimeField | auto_now=True    |

6. **PostEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_post_events'    |
| Post          | post          | ForeignKey    | to=Post, on_delete=models.CASCADE, related_name='post_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "post_events"      |

7. **CommentEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_comment_events'    |
| Post          | post          | ForeignKey    | to=Post, on_delete=models.CASCADE, related_name='comment_events'    |
| Comment       | comment       | ForeignKey    | to=Comment, on_delete=models.CASCADE, related_name='comment_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "comment_events"      |

8. **LikeDislikeEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_friend_request_events'    |
| Target        | target        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='targeted_friend_request_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "like_dislike"    |

9. **FriendEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_friend_events'    |
| Target        | target        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='targeted_friend_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "friend_added" |

10. **FriendRequestDeclinedEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_friend_request_declined_events'    |
| Target        | target        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='targeted_friend_request_declined_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "friend_request_declined"   |

11. **RemoveFriendEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_remove_friend_events'    |
| Target        | target        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='targeted_remove_friend_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "friend_removed"      |

12. **CommunityJoinEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_community_join_events'    |
| Community     | community     | ForeignKey    | to=Community, on_delete=models.CASCADE, related_name='community_join_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "community_join"     |

13. **CommunityLeaveEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_community_leave_events'    |
| Community     | community     | ForeignKey    | to=Community, on_delete=models.CASCADE, related_name='community_leave_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "community_leave"      |

14. **CommunityCreateEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_community_create_events'    |
| Community     | community     | ForeignKey    | to=Community, on_delete=models.CASCADE, related_name='community_create_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    |"community_create"      |

15. **CommunityDeleteEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_community_delete_events'    |
| Community     | community     | ForeignKey    | to=Community, on_delete=models.CASCADE, related_name='community_delete'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | community_delete"      |

16. **FriendRequestEvent Model**

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Initiator     | initiator     | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='initiated_friend_request_events'    |
| Target        | target        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='targeted_friend_request_events'    |
| Timestamp     | timestamp     | DateTimeField | auto_now_add=True    |
| Type          | type          | CharField    | "friend_request"      |
17. **FriendRequest Model**


| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| From Profile  | from_profile  | ForeignKey    | to=Profile, on_delete=models.CASCADE, related_name='friend_request_from_profile'    |
| To Profile    | to_profile    | ForeignKey    | to=Profile, on_delete=models.CASCADE, related_name='friend_request_to_profile'    |
| Sent On       | sent_on       | DateTimeField | auto_now_add=True    |
| Updated On    | updated_on    | DateTimeField | auto_now=True    |
| Accepted      | accepted      | BooleanField  | default=False    |
| Declined      | declined      | BooleanField  | default=False    |

18. **Post Model**

```Python
POST_TYPE_CHOICES = (
    (1, 'profile_wall'),
    (2, 'community_wall'),
)
```

| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Author        | author        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='posts'    |
| Content       | content       | TextField     | max_length=500    |
| Has Media     | has_media     | BooleanField  | default=False    |
| Image         | image         | CloudinaryField | 'post_image', folder = 'posts', null = True, blank = True   |
| Video         | video         | CloudinaryField |'post_video', folder = 'posts', null = True, blank = True   |
| Created On    | created_on    | DateTimeField | auto_now_add=True    |
| Updated On    | updated_on    | DateTimeField | auto_now=True    |
| Edited        | edited        | BooleanField  | default=False    |
| Post Type     | post_type     | IntegerField  | choices=POST_TYPE_CHOICES    |
| Community     | community     | ForeignKey    | to=Community, on_delete=models.CASCADE, related_name='posts'    |
| Profile       | profile       | ForeignKey    | to=Profile, on_delete=models.CASCADE, related_name='posts'    |
| Likes         | likes         | ManyToManyField | to=User, related_name='liked_posts'    |
| Dislikes      | dislikes      | ManyToManyField | to=User, related_name='disliked_posts'    |

19. **Comment Model**


| Name          | Database Key  | Field Type    | Validation |
| ------------- | ------------- | ------------- | ---------- |
| Author        | author        | ForeignKey    | to=User, on_delete=models.CASCADE, related_name='comments', null=True    |
| Post          | post          | ForeignKey    | to=Post, on_delete=models.CASCADE, related_name='comments'    |
| Content       | content       | TextField     | max_length=500    |
| Created On    | created_on    | DateTimeField | auto_now_add=True    |
| Updated On    | updated_on    | DateTimeField | auto_now=True    |
| Edited        | edited        | BooleanField  | default=False    |
| Likes         | likes         | ManyToManyField | to=User, related_name='liked_comments'    |
| Dislikes      | dislikes      | ManyToManyField | to=User, related_name='disliked_comments'    |








---
---
## Testing
Please refer to the [TESTING.md](TESTING.md) file for all test-related documentation.
---
## Deployment




















## Credits
- [Django](https://www.djangoproject.com/) for the framework.
- [Django-channels](https://channels.readthedocs.io/) for the real-time communication library.
- [Django-allauth](https://django-allauth.readthedocs.io/) for the authentication library.
- [BGJar](https://www.bgjar.com/): for the free access to the background images build tool.
- [Font awesome](https://fontawesome.com/): for the free access to icons.
- [Heroku](https://www.heroku.com/): for the free hosting of the website.
- [Cloudinary](https://cloudinary.com/): for the free access to the image hosting service.
- [Redis](https://redis.io/): for the free access to channel layer.
- [jQuery](https://jquery.com/): for providing varieties of tools to make standard HTML code look appealing.
- [jQuery UI](https://jqueryui.com/): for providing various tools to make interactive HTML code look appealing.
- [Coolors](https://coolors.co/): for providing a free platform to generate your own palette.
- [Postgresql](https://www.postgresql.org/): for providing a free database.
- [Responsive Viewer](https://chrome.google.com/webstore/detail/responsive-viewer/inmopeiepgfljkpkidclfgbgbmfcennb/related?hl=en): for providing a free platform to test website responsiveness
- [GoFullPage](chrome://extensions/?id=fdpohaocaechififmbbbbbknoalclacl): for allowing to create free full web page screenshots;
- [Favicon Generator. For real.](https://realfavicongenerator.net/): for providing a free platform to generate favicons.
- [getcssscan](https://getcssscan.com/css-box-shadow-examples/): for providing a free platform to generate CSS box shadow examples.
*All names are fictional and any resemblance to actual events or locales or persons, living or dead, is entirely coincidental.*
---
## Acknowledgments
- [Tim Nelson](https://github.com/TravelTimN), my mentor, who guided me through the development of the project with his advice.
- [Iuliia Konovalova](https://github.com/IuliiaKonovalova), my wife and my coding partner, who helped me to stay sane and happy during the project development, and helped me to choose the right styles and colors for the project design.