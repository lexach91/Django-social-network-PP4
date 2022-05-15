/* jshint esversion: 8, jquery: true, scripturl: true */
console.log('base.js');
$(document).ready(function() {
    
    // -------- posts, comments, profile functions --------
    $('.comments-container').hide();
    $('.post-form input[type="file"]').hide();    
    $('.post-form label[for="id_image"]').html('<i class="fas fa-paperclip"></i>');
    $('.post-form label[for="id_image"]').attr('title', 'Add an image');
    $('.post-form label[for="id_image"]').tooltip();
    
    const protocol = window.location.protocol;
    const host = window.location.host;
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    const commentFormHtml = `
        <input type="hidden" name="csrfmiddlewaretoken" value=${csrfToken}>
        <label for="id_content">Content:</label><textarea name="content" cols="40" rows="3" maxlength="500" required="" id="id_content" spellcheck="false"></textarea>
        <button type="submit" class="comment-submit">Comment</button>
    `;

    const postFormHtml = `
    <form class="post-form">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <label for="id_content">Content:</label><textarea name="content" cols="40" rows="3" maxlength="500" required="" id="id_content"></textarea>
        <label for="id_image" title="Add an image"><i class="fas fa-paperclip" aria-hidden="true"></i></label>
        <input type="file" name="image" accept="image/*" id="id_image" style="display: none;">
        <input type="hidden" name="post_type" id="id_post_type">
        <input type="hidden" name="community" id="id_community">
        <input type="hidden" name="profile" id="id_profile">
        <button type="submit" class="post-submit save-form">Post</button>
    </form>
    `;

    const createPostUrl = protocol + '//' + host + '/posts/create-post/';
    const likePostUrl = protocol + '//' + host + '/posts/like-post/';
    const dislikePostUrl = protocol + '//' + host + '/posts/dislike-post/';
    const createCommentUrl = protocol + '//' + host + '/posts/create-comment/';
    const likeCommentUrl = protocol + '//' + host + '/posts/like-comment/';
    const dislikeCommentUrl = protocol + '//' + host + '/posts/dislike-comment/';
    const editAvatarUrl = protocol + '//' + host + 'profiles/my_profile/edit-avatar/';
    const editAvatarBtn = $('.edit-avatar');
    const acceptAvatarBtn = $('.accept-avatar');
    const cancelAvatarBtn = $('.cancel-avatar');

    const createPost = (e) => {

        e.preventDefault();
        console.log('create post');
        console.log(createPostUrl);
        const form = $(e.target);
        let postType = $('input#post_type').val();
        let profileId = $('input#profile_id').val();
        let communityId = $('input#community_id').val();
        $('.post-form').find('input[name="post_type"]').val(postType);
        $('.post-form').find('input[name="profile"]').val(profileId);
        $('.post-form').find('input[name="community"]').val(communityId);
        
        let data = new FormData(form[0]);

        // make all inputs disabled
        $('.post-form input').attr('disabled', true);
        $('.post-form textarea').attr('disabled', true);
        $('.post-form button').attr('disabled', true);
        // add loading icon
        $('.post-form button').append('<i class="fas fa-spinner fa-spin"></i>');

        $.ajax({
            url: createPostUrl,
            type: 'POST',
            processData: false,
            contentType: false,
            cache: false,
            data: data,                
            success: (data) => {
                let post = data.post;
                console.log(post.avatar);
                let avatarUrl = post.avatar;
                let author = post.author;
                let authorUrl = post.author_url;
                let postContent = post.content;
                let createdAt = post.created_at;
                $('.post-wall').prepend(`
                    <div class="post" data-post-id='${post.id}'>
                        <div class="post-info">
                            <div class="post-author">
                                <img src="${avatarUrl}" alt="avatar" class="post-avatar">
                                <div class="post-author-name">
                                    <strong>
                                        <a href="${authorUrl}">
                                            ${author}
                                        </a>
                                    </strong>
                                </div>
                            </div>
                            <div class="post-time">
                                <em>Posted at ${createdAt}</em>
                            </div>
                        </div>
                        <div class="post-content">
                            <div class="post-text">
                                ${postContent}
                            </div>
                        </div>
                        <div class="likes-dislikes">
                            <div class="likes">
                                <i class="far fa-heart like-button" data-post-id="${post.id}"></i>
                                <span class="likes-count">0</span>
                            </div>
                            <div class="dislikes">
                                <i class="far fa-times-circle dislike-button" data-post-id="${post.id}"></i>
                                <span class="dislikes-count">0</span>
                            </div>
                            <div class="comments">
                                <i class="far fa-comment comment-button" data-post-id="${post.id}"></i>
                                <span class="comments-count">0</span>
                            </div>
                        </div>
                    </div>
                `);
                // check if the post has_media and if it does, add it to the .post-content before .post-text
                if(post.has_media) {
                    $(`.post[data-post-id='${post.id}'] .post-content`).prepend(`
                        <div class="post-media">
                            <img src="${post.image}" alt="post-image" class="post-image">
                        </div>
                    `);
                }
                
                $('.post-wall').find(`div[data-post-id='${post.id}']`).after(`
                    <div class="comments-container" data-for-post="${post.id}" style="display: none;">            
                        <form class="comment-form" data-post-id="${post.id}">` + commentFormHtml +                        
                        `</form>
                    </div>
                `);

                $('.post-form').find('textarea').val('');
                $(`.like-button[data-post-id='${post.id}']`).on('click', likeHandler);
                $(`.dislike-button[data-post-id='${post.id}']`).on('click', dislikeHandler);
                $(`.comment-button[data-post-id='${post.id}']`).on('click', commentHandler);
                $(`.comment-form[data-post-id='${post.id}']`).on('submit', createComment);
                $(`.post[data-post-id='${post.id}'] img.post-image`).on('click', toggleImage);
                // enable all inputs
                $('.post-form input').attr('disabled', false);
                $('.post-form textarea').attr('disabled', false);
                $('.post-form button').attr('disabled', false);
                // remove loading icon
                $('.post-form button i').remove();
                // if form has div.preview, replace it with <label for="id_image" title="Add an image"><i class="fas fa-paperclip" aria-hidden="true"></i></label>
                if($('.post-form').find('div.preview').length) {
                    $('.post-form').find('div.preview').replaceWith(`
                        <label for="id_image" title="Add an image"><i class="fas fa-paperclip" aria-hidden="true"></i></label>
                    `);
                    $('#id_image').on('change', imagePreview);
                }

            }
        });
    };

    const likeHandler = (e) =>{
        let postId = $(e.target).data('post-id');
        let commentId = $(e.target).data('comment-id');
        let url;
        if(commentId) {
            url = likeCommentUrl;
        } else {
            url = likePostUrl;
        }
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                post_id: postId,
                comment_id: commentId,
                csrfmiddlewaretoken: csrfToken
            },
            success: (data) => {
                let likesCount = data.likes_count;
                let dislikesCount = data.dislikes_count;
                let id = postId || commentId;
                let postOrComment = postId ? 'data-post-id=' : 'data-comment-id=';
                let selector = `i[${postOrComment}${id}]`;
                $(selector).parent().find('.likes-count').text(likesCount);
                $(selector).parent().find('.dislikes-count').text(dislikesCount);
                if(data.liked){
                    $(`${selector}.like-button`).removeClass('far').addClass('fas');
                    $(`${selector}.dislike-button`).removeClass('fas').addClass('far');
                } else if (data.disliked) {
                    $(`${selector}.like-button`).removeClass('far').addClass('fas');
                    $(`${selector}.dislike-button`).removeClass('fas').addClass('far');
                } else {
                    $(`${selector}.like-button`).removeClass('fas').addClass('far');
                    $(`${selector}.dislike-button`).removeClass('fas').addClass('far');
                }
            }
        });
    };

    const dislikeHandler = (e) => {
        let postId = $(e.target).data('post-id');
        let commentId = $(e.target).data('comment-id');
        let url;
        if(commentId) {
            url = dislikeCommentUrl;
        } else {
            url = dislikePostUrl;
        }
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                post_id: postId,
                comment_id: commentId,
                csrfmiddlewaretoken: csrfToken
            },
            success: (data) => {
                let likesCount = data.likes_count;
                let dislikesCount = data.dislikes_count;
                let id = postId || commentId;
                let postOrComment = postId ? 'data-post-id=' : 'data-comment-id=';
                let selector = `i[${postOrComment}${id}]`;
                $(selector).parent().find('.likes-count').text(likesCount);
                $(selector).parent().find('.dislikes-count').text(dislikesCount);
                if(data.liked){
                    $(`${selector}.like-button`).removeClass('far').addClass('fas');
                    $(`${selector}.dislike-button`).removeClass('fas').addClass('far');
                } else if (data.disliked) {
                    $(`${selector}.like-button`).removeClass('fas').addClass('far');
                    $(`${selector}.dislike-button`).removeClass('far').addClass('fas');
                } else {
                    $(`${selector}.like-button`).removeClass('fas').addClass('far');
                    $(`${selector}.dislike-button`).removeClass('fas').addClass('far');
                }
            }
        });
    };

    const commentHandler = (e) => {
        let postId = $(e.target).data('post-id');
        $(`div[data-for-post=${postId}]`).animate({
            height: 'toggle'
        }, 500);
    };

    const createComment = (e) =>{
        e.preventDefault();
        console.log(e.target);
        let postId = $(e.target).data('post-id');
        // console.log(postId);
        let commentContent = $(e.target).find('textarea').val();
        $.ajax({
            url: createCommentUrl,
            type: 'POST',
            data: {
                post_id: postId,
                comment_content: commentContent,
                csrfmiddlewaretoken: csrfToken
            },
            success: (data) => {
                let comment = data.comment;
                let avatarUrl = comment.avatar;                    
                let author = comment.author;
                let authorUrl = comment.author_url;
                let commentContent = comment.content;
                let createdAt = comment.created_at;
                let commentId = comment.id;
                let commentHtml = `
                    <div class="comment">
                        <div class="comment-info">
                            <div class="comment-author">
                                <img src="${avatarUrl}" alt="avatar" class="comment-avatar">
                                <div class="comment-author-name">
                                    <strong>
                                        <a href="${authorUrl}">
                                            ${author}
                                        </a>
                                    </strong>
                                </div>
                            </div>
                            <div class="comment-time">
                                <em>Posted at ${createdAt}</em>
                            </div>
                        </div>
                        <div class="comment-content">
                            <div class="comment-text">
                                ${commentContent}
                            </div>
                        </div>
                        <div class="likes-dislikes">
                            <div class="likes">
                                <i class="far fa-heart like-button" data-comment-id="${commentId}"></i>
                                <span class="likes-count">0</span>
                            </div>
                            <div class="dislikes">
                                <i class="far fa-times-circle dislike-button" data-comment-id="${commentId}"></i>
                                <span class="dislikes-count">0</span>
                            </div>
                        </div>
                    </div>
                `;
                let commentsContainer = $(`div[data-for-post=${postId}]`);
                let lastComment = commentsContainer.find('.comment').last();
                if(lastComment.length) {
                    lastComment.after(commentHtml);
                } else {
                    commentsContainer.prepend(commentHtml);
                }

                let commentCount = data.comment.comment_count;
                console.log(commentCount);
                let postElement = $(`.post[data-post-id=${postId}]`);
                postElement.find('.comments-count').text(commentCount);


                $(this).find('textarea').val('');
                $('.like-button').on('click', likeHandler);
                $('.dislike-button').on('click', dislikeHandler);
            }
        });
    };

    const toggleImage = (e) => {
        let postImage = $(e.target);
        postImage.toggleClass('full-height');
        // make post become bigger with the image
        postImage.parent().toggleClass('full-height');
    };

    const imagePreview = (e) => {
        // temporarily disable the event handler
        e.preventDefault();
        $('#id_image').off('change');
        // take the image from the file input and show it in the preview
        let file = e.target.files[0];
        let imgUrl = URL.createObjectURL(file);
        // create a new image element
        // let img = document.createElement('img');
        // img.src = imgUrl;
        // img.style.width = '100px';
        // img.style.height = '100px';
        // img.style.objectFit = 'cover';
        // img.style.objectPosition = 'center';
        // img.style.border = '1px solid #ccc';
        // img.style.position = 'relative';
        let previewDiv = document.createElement('div');
        previewDiv.classList.add('preview');
        previewDiv.style.width = '100px';
        previewDiv.style.height = '100px';
        previewDiv.style.border = '1px solid #ccc';
        previewDiv.style.position = 'relative';
        previewDiv.style.borderRadius = '0 0.7rem 0 0';
        previewDiv.style.alignSelf = 'start';
        // previewDiv.style.overflow = 'hidden';
        let img = document.createElement('img');
        img.src = imgUrl;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.style.objectPosition = 'center';
        previewDiv.appendChild(img);
        // create close button
        let closeButton = $('<i class="fas fa-times-circle"></i>');
        closeButton.css({
            position: 'absolute',
            top: '-8px',
            right: '-8px',
            cursor: 'pointer',
            color: '#ccc',
        });
        previewDiv.appendChild(closeButton[0]);
        // replace the fas-paperclip with the new image
        let labelBackup = $('label[for=id_image]');
        $('label[for=id_image]').replaceWith(previewDiv);
        // $(e.target).parent().find('i').replaceWith(previewDiv);
        // add event handler to the close button
        closeButton.on('click', () => {
            // remove the preview image
            $(e.target).parent().find('div.preview').replaceWith(labelBackup);
            // clear the file input
            $('#id_image').val('');            
            $('#id_image').on('change', imagePreview);            
        });
    };

    $('#id_image').on('change', imagePreview);

    $(editAvatarBtn).on('click', () => {
        // need to open select file dialog
        let fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.click();
        $(fileInput).on('change', (e) => {
            console.log(e.target.files[0]);
            console.log("file selected");
            // need to replace avatar image with selected file in the frontend
            let file = e.target.files[0];
            e.target.value = '';
            let currentAvatarUrl = $('img.avatar').attr('src');
            console.log(currentAvatarUrl);
            $('.avatar').attr('src', URL.createObjectURL(file));
            $(editAvatarBtn).addClass('hidden');
            $(acceptAvatarBtn).removeClass('hidden');
            $(cancelAvatarBtn).removeClass('hidden');
            $(cancelAvatarBtn).click(() => {
                $('.avatar').attr('src', currentAvatarUrl);
                $(editAvatarBtn).removeClass('hidden');
                $(acceptAvatarBtn).addClass('hidden');
                $(cancelAvatarBtn).addClass('hidden');
                $(fileInput).remove();
                $(fileInput).off('change');
                $(cancelAvatarBtn).off('click');
                $(acceptAvatarBtn).off('click');
            });
            $(acceptAvatarBtn).click(() => {
                let formData = new FormData();
                formData.append('avatar', file);
                formData.append('csrfmiddlewaretoken', csrfToken);
                $.ajax({
                    url: editAvatarUrl,
                    type: 'POST',
                    processData: false,
                    contentType: false,
                    cache: false,
                    data: formData,
                    success: (data) => {
                        console.log(data);
                        $(editAvatarBtn).removeClass('hidden');
                        $(acceptAvatarBtn).addClass('hidden');
                        $(cancelAvatarBtn).addClass('hidden');
                        // change avatar for this user in all posts
                        // $('img[src="' + currentAvatarUrl + '"]').attr('src', data.avatar_url);
                        $('.post[data-post-id]').each((index, element) => {
                            $(element).find('.post-avatar').attr('src', data.avatar_url);
                        });
                        // remove event handlers from accept and cancel buttons
                        $(acceptAvatarBtn).off('click');
                        $(cancelAvatarBtn).off('click');
                        $(fileInput).remove();
                    }
                });
            });
        });
    });

    $('.post-image').on('click', toggleImage);
    $('.post-form').on('submit', createPost);
    $('.like-button').on('click', likeHandler);
    $('.dislike-button').on('click', dislikeHandler);
    $('.comment-button').on('click', commentHandler);
    $('.comment-form').on('submit', createComment);

    // -------- friend requests functions -------- 

    const sendFriendRequestUrl = protocol + '//' + host + '/friends/send-friend-request/';
    const acceptFriendRequestUrl = protocol + '//' + host + '/friends/accept-friend-request/';
    const declineFriendRequestUrl = protocol + '//' + host + '/friends/decline-friend-request/';
    const removeFriendUrl = protocol + '//' + host + '/friends/remove-friend/';
    const cancelFriendRequestUrl = protocol + '//' + host + '/friends/cancel-friend-request/';

    const sendFriendRequest = (e) => {
        e.preventDefault();
        let profileId = $(e.target).data('profile-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        $.ajax({
            url: sendFriendRequestUrl,
            type: 'POST',
            data: {
                'profile_id': profileId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // change button text to 'Request pending'
                $(e.target).text('Request pending');
                // remove event handler from the button
                $(e.target).off('click');
                // add .cancel-friend-button next to the button
                let cancelFriendButton = $('<button class="cancel-friend-button" data-profile-id="' + profileId + '">Cancel</button>');
                $(e.target).after(cancelFriendButton);
                // add event handler to the cancel button
                $(cancelFriendButton).on('click', cancelFriendRequest);
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
            }
        });
    };

    const cancelFriendRequest = (e) => {
        e.preventDefault();
        let profileId = $(e.target).data('profile-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        $.ajax({
            url: cancelFriendRequestUrl,
            type: 'POST',
            data: {
                'profile_id': profileId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // remove cancel button
                $(e.target).remove();
                // change .send-friend-button next to the button to 'Add to friends'
                $('.send-friend-button[data-profile-id="' + profileId + '"]').text('Add to friends');
                // make it enabled again
                $('.send-friend-button[data-profile-id="' + profileId + '"]').attr('disabled', false);
                // add event handler to the button
                $('.send-friend-button[data-profile-id="' + profileId + '"]').on('click', sendFriendRequest);
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
            }
        });
    };

    const acceptFriendRequest = (e) => {
        e.preventDefault();
        let profileId = $(e.target).data('profile-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // make decline button disabled
        $('.decline-friend-button[data-profile-id="' + profileId + '"]').attr('disabled', true);
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        $.ajax({
            url: acceptFriendRequestUrl,
            type: 'POST',
            data: {
                'profile_id': profileId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // replace accept and decline buttons with .chat-button link and .unfriend-button
                let username = $('input[id="profile_username"]').val();
                let chatUrl = protocol + '//' + host + '/chat-with-' + username + '/';
                let chatButton = $('<a class="chat-button" href="' + chatUrl + '">Chat</a>');
                let unfriendButton = $('<button class="unfriend-button" data-profile-id="' + profileId + '">Unfriend</button>');
                $(e.target).replaceWith(chatButton);
                $('.decline-friend-button[data-profile-id="' + profileId + '"]').replaceWith(unfriendButton);
                // add event handler to the unfriend button
                $(unfriendButton).on('click', unfriend);
                // prepend post form to .profile-wall
                $('.profile-wall').prepend(postFormHtml);
                // add event handlers to the post form
                $('.post-form').on('submit', createPost);
                $('#id_image').on('change', imagePreview);
                // for each post in the wall add a comment form html
                $('.post').each(function () {
                    let postId = $(this).data('post-id');
                    let commentForm = `<form class="comment-form" data-post-id="${postId}">` +
                        commentFormHtml +
                        `</form>`;
                    // append the comment form to the .comments-container that follows the post
                    $('.comments-container[data-for-post="' + postId + '"]').append(commentForm);
                });
                $('.comment-form').on('submit', createComment);
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
                // enable decline button
                $('.decline-friend-button[data-profile-id="' + profileId + '"]').attr('disabled', false);
            }
        });
    };

    const declineFriendRequest = (e) => {
        e.preventDefault();
        let profileId = $(e.target).data('profile-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // make accept button disabled
        $('.accept-friend-button[data-profile-id="' + profileId + '"]').attr('disabled', true);
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        $.ajax({
            url: declineFriendRequestUrl,
            type: 'POST',
            data: {
                'profile_id': profileId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // replace accept and decline buttons with .send-friend-button
                let sendFriendButton = $('<button class="send-friend-button" data-profile-id="' + profileId + '">Add to friends</button>');
                $(e.target).replaceWith(sendFriendButton);
                $('.accept-friend-button[data-profile-id="' + profileId + '"]').remove();
                // add event handler to the send friend button
                $(sendFriendButton).on('click', sendFriendRequest);
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
                // enable accept button
                $('.accept-friend-button[data-profile-id="' + profileId + '"]').attr('disabled', false);
            }
        });
    };

    const unfriend = (e) => {
        e.preventDefault();
        let profileId = $(e.target).data('profile-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // make .chat-button link disabled
        let chatHrefBackup = $('.chat-button').attr('href');
        $('.chat-button').attr('href', "javascript:void(0);");
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        // make all .post-form and .comment-form inputs, buttons, and textareas disabled
        $('.post-form').find('input, button, textarea').attr('disabled', true);
        $('.comment-form').find('input, button, textarea').attr('disabled', true);
        $.ajax({
            url: removeFriendUrl,
            type: 'POST',
            data: {
                'profile_id': profileId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // remove unfriend button
                $(e.target).remove();
                // replace .chat-button link with .send-friend-button
                let sendFriendButton = $('<button class="send-friend-button" data-profile-id="' + profileId + '">Add to friends</button>');
                $('.chat-button').replaceWith(sendFriendButton);
                // add event handler to the send friend button
                $(sendFriendButton).on('click', sendFriendRequest);
                // remove all .post-form and .comment-form inputs, buttons, and textareas
                $('.post-form').remove();
                $('.comment-form').remove();
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
                // enable .chat-button link
                $('.chat-button').attr('href', chatHrefBackup);
                // enable all .post-form and .comment-form inputs, buttons, and textareas
                $('.post-form').find('input, button, textarea').attr('disabled', false);
                $('.comment-form').find('input, button, textarea').attr('disabled', false);
            }
        });
    };

    $('.send-friend-button').on('click', sendFriendRequest);
    $('.cancel-friend-button').on('click', cancelFriendRequest);
    $('.accept-friend-button').on('click', acceptFriendRequest);
    $('.decline-friend-button').on('click', declineFriendRequest);
    $('.unfriend-button').on('click', unfriend);

    // -------- Community functions -------- 
    const joinCommunityUrl = protocol + '//' + host + window.location.pathname + 'join/';
    const leaveCommunityUrl = protocol + '//' + host + window.location.pathname + 'leave/';

    const joinCommunity = (e) => {
        e.preventDefault();
        let communityId = $(e.target).data('community-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        $.ajax({
            url: joinCommunityUrl,
            type: 'POST',
            data: {
                'community_id': communityId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // replace join community button with leave community button
                let leaveCommunityButton = $('<button class="leave-community-button" data-community-id="' + communityId + '">Leave community</button>');
                $(e.target).replaceWith(leaveCommunityButton);
                // add event handler to the leave community button
                $(leaveCommunityButton).on('click', leaveCommunity);
                // add post and comment forms to the community page
                // prepend post form to .profile-wall
                $('.profile-wall').prepend(postFormHtml);
                // add event handlers to the post form
                $('.post-form').on('submit', createPost);
                $('#id_image').on('change', imagePreview);
                // for each post in the wall add a comment form html
                $('.post').each(function () {
                    let postId = $(this).data('post-id');
                    let commentForm = `<form class="comment-form" data-post-id="${postId}">` +
                        commentFormHtml +
                        `</form>`;
                    // append the comment form to the .comments-container that follows the post
                    $('.comments-container[data-for-post="' + postId + '"]').append(commentForm);
                });
                $('.comment-form').on('submit', createComment);
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
            }
        });
    };

    const leaveCommunity = (e) => {
        e.preventDefault();
        let communityId = $(e.target).data('community-id');
        // make e.target disabled
        $(e.target).attr('disabled', true);
        // show loading icon
        $(e.target).append('<i class="fas fa-spinner fa-spin"></i>');
        $.ajax({
            url: leaveCommunityUrl,
            type: 'POST',
            data: {
                'community_id': communityId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: (data) => {
                console.log(data);
                // replace leave community button with join community button
                let joinCommunityButton = $('<button class="join-community-button" data-community-id="' + communityId + '">Join community</button>');
                $(e.target).replaceWith(joinCommunityButton);
                // add event handler to the join community button
                $(joinCommunityButton).on('click', joinCommunity);
                // remove all .post-form and .comment-form inputs, buttons, and textareas
                $('.post-form').remove();
                $('.comment-form').remove();
            },
            error: (data) => {
                console.log(data);
                // remove loading icon
                $(e.target).find('i').remove();
                // enable e.target
                $(e.target).attr('disabled', false);
            }
        });
    };

    $('.join-community-button').on('click', joinCommunity);
    $('.leave-community-button').on('click', leaveCommunity);

}); // end of document ready