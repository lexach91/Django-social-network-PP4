/* jshint esversion: 6, jquery: true */
$(document).ready(function () {
    const roomName = $('input#userUsername').val();
    const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const notificationSocket = new WebSocket(socketProtocol + '//' + window.location.host + '/ws/notifications/' + roomName + '/');

    const updateFriendRequests = function (num) {
        if (num > 0) {
            $('.nav-badge.requests-count').text(`(${num})`);
        }
        // highlight it
        $('.nav-badge.requests-count').effect('highlight', {
            color: '#ff0000'
        }, 1000);
    };

    const updateMessagesCount = function (data) {
        if (data.unread_messages > 0) {
            $('.nav-badge.messages-count').text(`(${data.unread_messages})`);
            $('.message-count[data-chat-id="' + data.chat_id + '"]').text(`(${data.unread_messages})`);
            $('.message-count[data-chat-id="' + data.chat_id + '"]').removeClass('hidden');
            $('.message-last-message[data-chat-id="' + data.chat_id + '"]').text(data.message);
        }
        // highlight it
        $('.nav-badge.messages-count').effect('highlight', {
            color: '#ff0000'
        }, 1000);
    };

    notificationSocket.onopen = function () {
        console.log('Notification socket opened');
    };

    notificationSocket.onclose = function () {
        console.log('Notification socket closed');
    };

    notificationSocket.onerror = function () {
        console.log('Notification socket error');
    };

    notificationSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.data.unread_messages) {
            updateMessagesCount(data.data);
        } else if (data.data.pending_requests) {
            updateFriendRequests(data.data.pending_requests);
        }
    };

}); // end of document ready