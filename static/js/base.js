/* jshint esversion: 8, jquery: true, scripturl: true */
$(document).ready(function() {
    
    // Tooltip to all elements that have a title attribute
    $('*[title]').tooltip();

    // -------- posts, comments, profile functions --------
    $('.comments-container').hide();
    $('.post-form input[type="file"]').hide();    
    $('.post-form label[for="id_image"]').html('<i class="fas fa-paperclip"></i>');
    $('.post-form label[for="id_image"]').attr('title', 'Add an image to your post');
    
    const protocol = window.location.protocol;
    const host = window.location.host;
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    const commentFormHtml = `
        <input type="hidden" name="csrfmiddlewaretoken" value=${csrfToken}>
        <label for="id_content">Content:</label><textarea name="content" cols="40" rows="3" maxlength="500" required="" id="id_content" spellcheck="false"></textarea>
        <button type="submit" class="comment-submit">Comment</button>
    `;

    const postFormHtml = `
    <form class="post-form create">
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

    const editPostFormHtml = `
    <form class="post-form edit" data-post-id="">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <textarea name="content" cols="40" rows="3" maxlength="500" required="" id="id_content"></textarea>
        <label for="post_file" title="Add an image"><i class="fas fa-paperclip" aria-hidden="true"></i></label>
        <input type="file" name="image" accept="image/*" id="post_file" style="display: none;">        
        <button class="cancel-edit-button" type="button">Cancel</button>
        <button type="submit" class="post-edit-submit save-form">Save</button>
        <input type="hidden" name="post_id" id="id_post_id">
        <input type="hidden" name="post_type" id="id_post_type">
        <input type="hidden" name="community" id="id_community">
        <input type="hidden" name="profile" id="id_profile">
    </form>
    `;

    const editCommentFormHtml = `
    <form class="comment-form edit" data-comment-id="">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <textarea name="content" cols="40" rows="3" maxlength="500" required="" id="id_content"></textarea>
        <button class="cancel-edit-button" type="button">Cancel</button>
        <button type="submit" class="comment-edit-submit save-form">Save</button>
    </form>`;


    const createPostUrl = protocol + '//' + host + '/posts/create-post/';
    const editPostUrl = protocol + '//' + host + '/posts/edit-post/';
    const deletePostUrl = protocol + '//' + host + '/posts/delete-post/';
    const likePostUrl = protocol + '//' + host + '/posts/like-post/';
    const dislikePostUrl = protocol + '//' + host + '/posts/dislike-post/';
    const createCommentUrl = protocol + '//' + host + '/posts/create-comment/';
    const editCommentUrl = protocol + '//' + host + '/posts/edit-comment/';
    const deleteCommentUrl = protocol + '//' + host + '/posts/delete-comment/';
    const likeCommentUrl = protocol + '//' + host + '/posts/like-comment/';
    const dislikeCommentUrl = protocol + '//' + host + '/posts/dislike-comment/';
    const editAvatarUrl = protocol + '//' + host + '/profiles/my_profile/edit_avatar/';
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
                $('.no-posts').remove();
                let post = data.post;
                console.log(post);
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
                        <div class="author-options">
                            <i class="fas fa-edit edit-post-button" data-post-id="${post.id}" aria-hidden="true"></i>
                            <i class="fas fa-trash-alt delete-post-button" data-post-id="${post.id}" aria-hidden="true"></i>
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
                $(`.edit-post-button[data-post-id='${post.id}']`).on('click', toggleEditPost);
                $(`.delete-post-button[data-post-id='${post.id}']`).on('click', toggleDeletePost);
                // enable all inputs
                $('.post-form input').attr('disabled', false);
                $('.post-form textarea').attr('disabled', false);
                $('.post-form button').attr('disabled', false);
                // remove loading icon
                $('.post-form button i').remove();
                if($('.post-form').find('div.preview').length) {
                    $('.post-form').find('div.preview').replaceWith(`
                        <label for="id_image" title="Add an image"><i class="fas fa-paperclip" aria-hidden="true"></i></label>
                    `);
                    $('#id_image').on('change', imagePreview);
                }

            }
        });
    };

    const editPost = (e, postBackup) => {
        e.preventDefault();
        const form = $(e.target);
        let postId = $(postBackup).data('post-id');
        $(form).find('input[name="image"]').attr('id', 'id_image');
        let postType = $('input#post_type').val();
        let profileId = $('input#profile_id').val();
        let communityId = $('input#community_id').val();
        $(form).find('input[name="post_type"]').val(postType);
        $(form).find('input[name="profile"]').val(profileId);
        $(form).find('input[name="community"]').val(communityId);
        let data = new FormData(form[0]);
        let new_content = $(form).find('textarea[name="content"]').val();
        let new_image = $(form).find('input[name="image"]').val();
        let had_image = $(postBackup).find('img.post-image').length;
        data.append('post_id', postId);
        // rename form's file input id from post_file to id_image

        // make all inputs disabled
        $(e.target).find('input').attr('disabled', true);
        $(e.target).find('textarea').attr('disabled', true);
        $(e.target).find('button').attr('disabled', true);
        // add loading icon
        $(e.target).find('.save-form').append('<i class="fas fa-spinner fa-spin"></i>');

        $.ajax({
            url: editPostUrl,
            type: 'POST',
            processData: false,
            contentType: false,
            cache: false,
            data: data,
            success: (data) => {
                console.log(data);
                postBackup.find('.post-text').html(new_content);
                if(new_image) {
                    if(had_image) {
                        postBackup.find('.post-media img').attr('src', data.image);
                    } else {
                        postBackup.find('.post-content').prepend(`
                        <div class="post-media">
                            <img src="${data.image}" alt="post-image" class="post-image">
                        </div>
                        `);      
                    }
                }
                if(had_image && !data.image) {
                    postBackup.find('.post-media').remove();
                }
                let editedAt = new Date().toLocaleString();
                postBackup.find('.post-time em').text(`Edited at ${editedAt}`);
                // replace the form with the postBackup
                $(e.target).replaceWith(postBackup);
                // add event listeners to likes, dislikes, comments, edit, delete, and imageToggle
                $(`.like-button[data-post-id='${postId}']`).on('click', likeHandler);
                $(`.dislike-button[data-post-id='${postId}']`).on('click', dislikeHandler);
                $(`.comment-button[data-post-id='${postId}']`).on('click', commentHandler);
                $('.edit-post-button[data-post-id=' + postId + ']').on('click', toggleEditPost);
                $('.delete-post-button[data-post-id=' + postId + ']').on('click', toggleDeletePost);
                $('.post-image').on('click', toggleImage);
                // remove .cover div and restore scroll for the page
                $('.cover').remove();
                $('body').css('overflow', 'auto');
            },
            error: (data) => {
                console.log(data);
                // enable all inputs
                $(e.target).find('input').attr('disabled', false);
                $(e.target).find('textarea').attr('disabled', false);
                $(e.target).find('button').attr('disabled', false);
                // remove loading icon
                $(e.target).find('.save-form i').remove();

            }
        });
    };

    const deletePost = (e) => {
        e.preventDefault();
        let postId = $(e.target).data('post-id');
        let post = $(`.post[data-post-id='${postId}']`);
        // need to cover the post with a transparent div with a spinner icon
        let spinner = `
            <div class="spinner-container">
                <i class="fas fa-spinner fa-spin"></i>
            </div>
        `;
        post.append(spinner);
        // make post's position relative and spinner-container absolute
        post.css('position', 'relative');
        $('.spinner-container').css('position', 'absolute');
        // let spinner container to cover the post
        $('.spinner-container').css({
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'z-index': '100',
            'background-color': 'rgba(0,0,0,0.5)',
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        });
        
        $.ajax({
            url: deletePostUrl,
            type: 'POST',
            data: {
                'post_id': postId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: (data) => {
                console.log(data);
                post.remove();

                $(`.comments-container[data-for-post='${postId}']`).remove();
            },
            error: (data) => {
                console.log(data);
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
                'post_id': postId,
                'comment_id': commentId,
                'csrfmiddlewaretoken': csrfToken
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
                'post_id': postId,
                'comment_id': commentId,
                'csrfmiddlewaretoken': csrfToken
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
                'post_id': postId,
                'comment_content': commentContent,
                'csrfmiddlewaretoken': csrfToken
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
                        <div class="author-options">
                            <i class="fas fa-edit edit-comment-button" data-comment-id="${commentId}" aria-hidden="true"></i>
                            <i class="fas fa-trash-alt delete-comment-button" data-comment-id="${commentId}" aria-hidden="true"></i>
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
                $('.edit-comment-button').on('click', toggleEditComment);
                $('.delete-comment-button').on('click', toggleDeleteComment);
            }
        });
    };

    const editComment = (e, commentBackup) => {
        e.preventDefault();
        const form = $(e.target);
        const commentId = $(commentBackup).data('comment-id');
        const data = {
            'comment_id': commentId,
            'comment_content': form.find('textarea').val(),
            'csrfmiddlewaretoken': csrfToken
        };
        console.log(data);
        let new_content = $(form).find('textarea').val();
        // data.append('comment_id', commentId);
        // make all inputs disabled
        form.find('textarea').prop('disabled', true);
        form.find('button').prop('disabled', true);
        // add loading icon
        $(e.target).find('.save-form').append(`<i class="fas fa-spinner fa-spin"></i>`);
        $.ajax({
            url: editCommentUrl,
            type: 'POST',
            data: data,
            success: (data) => {
                commentBackup.find('.comment-content').html(new_content);
                let editedAt = new Date().toLocaleString();
                commentBackup.find('.comment-time').find('em').text(`Edited at ${editedAt}`);
                $(e.target).replaceWith(commentBackup);
                $('.like-button[data-comment-id=' + commentId + ']').on('click', likeHandler);
                $('.dislike-button[data-comment-id=' + commentId + ']').on('click', dislikeHandler);
                $('.edit-comment-button[data-comment-id=' + commentId + ']').on('click', toggleEditComment);
                $('.delete-comment-button[data-comment-id=' + commentId + ']').on('click', toggleDeleteComment);
                // remove .cover div and restore scroll
                $('.cover').remove();
                $('body').css('overflow', 'auto');
            },
            error: (data) => {
                console.log(data);
                $(e.target).find('.save-form').find('i').remove();
                form.find('textarea').prop('disabled', false);
                form.find('button').prop('disabled', false);
            }
        });
    };

    const deleteComment = (e) => {
        e.preventDefault();
        let commentId = $(e.target).data('comment-id');
        let comment = $('.comment[data-comment-id=' + commentId + ']');
        let spinner = `
            <div class="spinner-container">
                <i class="fas fa-spinner fa-spin"></i>
            </div>
        `;
        comment.append(spinner);
        comment.css('position', 'relative');
        $('.spinner-container').css({
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'z-index': '100',
            'background-color': 'rgba(0, 0, 0, 0.5)',
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        });
        $.ajax({
            url: deleteCommentUrl,
            type: 'POST',
            data: {
                'comment_id': commentId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: (data) => {
                comment.remove();
                let postId = data.post_id;
                let postElement = $(`.post[data-post-id=${postId}]`);
                let commentCount = data.comment_count;
                postElement.find('.comments-count').text(commentCount);
            },
            error: (data) => {
                console.log(data);
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
        let labelBackup = $(e.target).prev().clone();
        $(e.target).prev().replaceWith(previewDiv);
        // $(e.target).parent().find('i').replaceWith(previewDiv);
        // add event handler to the close button
        closeButton.on('click', () => {
            // remove the preview image
            $(e.target).parent().find('div.preview').replaceWith(labelBackup);
            // clear the file input
            $(e.target).val('');        
            $(e.target).on('change', imagePreview);
        });
    };

    const toggleEditPost = (e) => {
        e.preventDefault();
        let postId = $(e.target).attr('data-post-id');
        let postBackup = $('.post[data-post-id="' + postId + '"]');
        let formElement = editPostFormHtml.replace('data-post-id=""', 'data-post-id="' + postId + '"');
        let lastPostOnThePage = $('.post').last();
        $('.post[data-post-id="' + postId + '"]').replaceWith(formElement);
        if (postBackup[0] === lastPostOnThePage[0]) {
            console.log('last post');
            $('.post-form.edit[data-post-id="' + postId + '"]').css('margin-bottom', '7em');
        }
        // insert the .post-text from the backup post into the edit post form textarea
        $('.post-form.edit[data-post-id="' + postId + '"]').find('textarea').val(postBackup.find('.post-text').text().trim());
        // need to check if postBackup had an image
        if(postBackup.find('.post-image').length > 0) {
            console.log('image found');
            // need to create an image preview for the edit post form
            let previewDiv = document.createElement('div');
            previewDiv.classList.add('preview');
            previewDiv.style.width = '100px';
            previewDiv.style.height = '100px';
            previewDiv.style.border = '1px solid #ccc';
            previewDiv.style.position = 'relative';
            previewDiv.style.borderRadius = '0 0.7rem 0 0';
            previewDiv.style.alignSelf = 'start';
            let img = document.createElement('img');
            img.src = postBackup.find('.post-image').attr('src');
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover';
            img.style.objectPosition = 'center';
            previewDiv.appendChild(img);
            let closeButton = $('<i class="fas fa-times-circle"></i>');
            closeButton.css({
                position: 'absolute',
                top: '-8px',
                right: '-8px',
                cursor: 'pointer',
                color: '#ccc',
            });
            previewDiv.appendChild(closeButton[0]);
            let labelBackup = $('.post-form.edit[data-post-id="' + postId + '"]').find('label[for=post_file]');
            $('.post-form.edit[data-post-id="' + postId + '"]').find('label[for=post_file]').replaceWith(previewDiv);
            





            // add event handler to the close button
            closeButton.on('click', () => {
                // remove the preview image
                $('.post-form.edit[data-post-id="' + postId + '"]').find('div.preview').replaceWith(labelBackup);
                
                // clear the file input
                $('.post-form.edit[data-post-id="' + postId + '"]').find('input[type=file]').val('');
                $('.post-form.edit[data-post-id="' + postId + '"]').find('input[type=file]').on('change', imagePreview);
            });

        } else {
            console.log('no image found');
            $('.post-form.edit[data-post-id="' + postId + '"]').find('input[type=file]').on('change', imagePreview);
        }
        // need to create a div that will cover all the page except the edit post form
        let coverDiv = document.createElement('div');
        coverDiv.classList.add('cover');
        coverDiv.style.position = 'fixed';
        coverDiv.style.top = '0';
        coverDiv.style.left = '0';
        coverDiv.style.width = '100%';
        coverDiv.style.height = '100%';
        coverDiv.style.backgroundColor = 'rgba(0,0,0,0.5)';
        coverDiv.style.zIndex = '10';
        
        // add the cover div to the body
        $('body').append(coverDiv);
        // scroll the page so that the edit post form is in the middle of the page
        $(document).scrollTop($('.post-form.edit[data-post-id="' + postId + '"]').offset().top - $(window).height() / 2);
        // make form z-index higher than the cover div
        $('.post-form.edit[data-post-id="' + postId + '"]').css('z-index', '11');
        // if this is the last post on the page add margin-bottom to the edit post form
        // prevent the page from scrolling
        $('body').css('overflow', 'hidden');
        

        // need to add event handler to the cancel button
        $('.post-form.edit[data-post-id="' + postId + '"]').find('.cancel-edit-button').on('click', () => {
            $('.post-form.edit[data-post-id="' + postId + '"]').replaceWith(postBackup);
            $('.edit-post-button[data-post-id="' + postId + '"]').on('click', toggleEditPost);
            $('.like-button[data-post-id="' + postId + '"]').on('click', likeHandler);
            $('.dislike-button[data-post-id="' + postId + '"]').on('click', dislikeHandler);
            $('.comment-button[data-post-id="' + postId + '"]').on('click', commentHandler);
            $('.delete-post-button[data-post-id="' + postId + '"]').on('click', deletePost);
            // remove the cover div
            $('.cover').remove();
            // allow the page to scroll
            $('body').css('overflow', 'auto');
            
        });

        // need to add event handler to form submit
        $('.post-form.edit[data-post-id="' + postId + '"]').on('submit', (e) => {
            editPost(e, postBackup);
        });
    };

    const toggleDeletePost = (e) => {
        // need to ask for confirmation with popup
        let confirmDelete = confirm('Are you sure you want to delete this post?');
        if (confirmDelete) {
            deletePost(e);
        } else {
            // do nothing
            console.log('cancelled');
        }
    };

    const toggleEditComment = (e) => {
        e.preventDefault();
        let commentId = $(e.target).attr('data-comment-id');
        let commentBackup = $('.comment[data-comment-id="' + commentId + '"]');
        let formElement = editCommentFormHtml.replace('data-comment-id=""', 'data-comment-id="' + commentId + '"');
        $('.comment[data-comment-id="' + commentId + '"]').replaceWith(formElement);
        // insert the .comment-text from the backup comment into the edit comment form textarea
        $('.comment-form.edit[data-comment-id="' + commentId + '"]').find('textarea').val(commentBackup.find('.comment-content').text().trim());
        
        // need to create a div that will cover all the page except the edit post form
        let coverDiv = document.createElement('div');
        coverDiv.classList.add('cover');
        coverDiv.style.position = 'fixed';
        coverDiv.style.top = '0';
        coverDiv.style.left = '0';
        coverDiv.style.width = '100%';
        coverDiv.style.height = '100%';
        coverDiv.style.backgroundColor = 'rgba(0,0,0,0.5)';
        coverDiv.style.zIndex = '10';
        
        // add the cover div to the body
        $('body').append(coverDiv);
        // scroll the page so that the edit comment form is in the middle of the page
        $(document).scrollTop($('.comment-form.edit[data-comment-id="' + commentId + '"]').offset().top - $(window).height() / 2);
        // make form z-index higher than the cover div
        $('.comment-form.edit[data-comment-id="' + commentId + '"]').css('z-index', '11');
        // prevent the page from scrolling
        $('body').css('overflow', 'hidden');
        
        
        
        
        
        // add event handler to the cancel button
        $('.comment-form.edit[data-comment-id="' + commentId + '"]').find('.cancel-edit-button').on('click', () => {
            $('.comment-form.edit[data-comment-id="' + commentId + '"]').replaceWith(commentBackup);
            $('.edit-comment-button[data-comment-id="' + commentId + '"]').on('click', toggleEditComment);
            $('.delete-comment-button[data-comment-id="' + commentId + '"]').on('click', toggleDeleteComment);
            // recover event handler for like and dislike buttons
            $('.like-button[data-comment-id="' + commentId + '"]').on('click', likeHandler);
            $('.dislike-button[data-comment-id="' + commentId + '"]').on('click', dislikeHandler);
            // remove the cover div
            $('.cover').remove();
            // allow the page to scroll
            $('body').css('overflow', 'auto');
        });
        // need to add event handler to form submit
        $('.comment-form.edit[data-comment-id="' + commentId + '"]').on('submit', (e) => {
            editComment(e, commentBackup);
        });

    };

    const toggleDeleteComment = (e) => {
        // need to ask for confirmation with popup
        let confirmDelete = confirm('Are you sure you want to delete this comment?');
        if (confirmDelete) {
            deleteComment(e);
        } else {
            // do nothing
            console.log('cancelled');
        }
    };

    $('#id_image').on('change', imagePreview);

    $(editAvatarBtn).on('click', () => {
        // need to open select file dialog
        let fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.click();
        let file;
        $(fileInput).on('change', (e) => {
            console.log(e.target.files[0]);
            console.log("file selected");
            // need to replace avatar image with selected file in the frontend
            file = e.target.files[0];
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
            $(acceptAvatarBtn).on('click', () => {
                console.log("accept avatar");
                let formData = new FormData();
                formData.append('avatar', file);
                formData.append('csrfmiddlewaretoken', csrfToken);
                console.log(formData);
                console.log(csrfToken);
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
                        $('.post').each((index, element) => {
                            $(element).find('.post-avatar[src="' + currentAvatarUrl + '"]').attr('src', data.avatar_url);
                        });
                        // remove event handlers from accept and cancel buttons
                        $(acceptAvatarBtn).off('click');
                        $(cancelAvatarBtn).off('click');
                        $(fileInput).remove();
                    },
                    error: (data) => {
                        console.log(data);
                    }
                });
            });
        });
    });

    $('.post-image').on('click', toggleImage);
    $('.post-form.create').on('submit', createPost);
    $('.like-button').on('click', likeHandler);
    $('.dislike-button').on('click', dislikeHandler);
    $('.comment-button').on('click', commentHandler);
    $('.comment-form').on('submit', createComment);

    $('.edit-post-button').on('click', toggleEditPost);
    $('.delete-post-button').on('click', toggleDeletePost);
    $('.edit-comment-button').on('click', toggleEditComment);
    $('.delete-comment-button').on('click', toggleDeleteComment);
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
                let chatUrl = protocol + '//' + host + '/my_messages/chat-with-' + username + '/';
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
                // if there's .no-posts div change it p inner text to '<p>You can post something to make  ${user_profile}  notice you</p>'
                if ($('.no-posts').length) {
                    let name = $('.profile-name').text().replace(/\n/g, '').replace(/Name:/, '').trim();
                    let text = '<p>You can post something to make ' + name + ' notice you</p>';
                    $('.no-posts').html(text);
                }
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
                if ($('.no-posts').length) {
                    let text = '<p>You need to add this person to friends to start posting here</p>';
                    $('.no-posts').html(text);
                }
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
                let leaveCommunityButton = $('<button class="leave-community-button" data-community-id="' + communityId + '">Leave community <i class="fas fa-sign-out-alt"></button>');
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
                if($('.no-posts').length) {
                    $('.no-posts').html('<p>You can start posting to share your thoughts with the community</p>');
                }
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
                let joinCommunityButton = $('<button class="join-community-button" data-community-id="' + communityId + '">Join community <i class="fas fa-sign-in-alt"></button>');
                $(e.target).replaceWith(joinCommunityButton);
                // add event handler to the join community button
                $(joinCommunityButton).on('click', joinCommunity);
                // remove all .post-form and .comment-form inputs, buttons, and textareas
                $('.post-form').remove();
                $('.comment-form').remove();
                if ($('.no-posts').length) {
                    let text = '<p>You need to join this community to start posting here</p>';
                    $('.no-posts').html(text);
                }
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