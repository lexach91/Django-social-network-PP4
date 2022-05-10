/* jshint esversion: 8, jquery: true */
console.log('base.js');
$(document).ready(function() {
// posts, comments, profile functions
    $('.comments-container').hide();

    // make file input in post form look like a paperclip
    $('.post-form input[type="file"]').hide();
    
    $('.post-form label[for=id_image]').html('<i class="fas fa-paperclip"></i>');
    
    const protocol = window.location.protocol;
    const host = window.location.host;
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    const commentFormHtml = `
        <input type="hidden" name="csrfmiddlewaretoken" value=${csrfToken}>
        <label for="id_content">Content:</label><textarea name="content" cols="40" rows="3" maxlength="500" required="" id="id_content" spellcheck="false"></textarea>
        <button type="submit" class="comment-submit">Comment</button>
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
    }


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

}); // end of document ready