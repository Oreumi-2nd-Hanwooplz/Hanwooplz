document.addEventListener('DOMContentLoaded', function () {
    var commentForm = document.querySelector('form');
    var commentText = document.getElementById('comment-input');
    var submitButton = document.getElementById('submit-button');
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    function fetchComments() {
        fetch('/api/comments/')
            .then(function (response) {
                return response.json();
            })
            .then(function (comments) {
                
                //commentList.innerHTML = '';
                comments.forEach(function (comment) {
                    displayComments(comment);
                });
            })
            .catch(function (error) {
                alert('댓글을 가져오는 데 실패했습니다.');
            });
    }

    submitButton.addEventListener('click', function () {
        var commentData = {
            content: commentText.value
        };

        fetch('/api/comments/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(commentData),
        })
            .then(function (response) {
                if (response.status === 201) {
                    commentText.value = '';
                    commentData.author = author_name;
                    displayComments(commentData);
                } else {
                    alert('댓글 작성에 실패했습니다.');
                }
            });
    });

    function displayComments(comment) {
        var commentList = document.querySelector('.comment-container');

        var commentBox = document.createElement('div');
        commentBox.classList.add('comment-box');

        // 댓글 작성자
        var commentAuthor = document.createElement('div');
        commentAuthor.classList.add('comment-author');
        commentAuthor.textContent = comment.author;

        // 댓글 내용
        var commentContent = document.createElement('div');
        commentContent.classList.add('comment-content');
        commentContent.textContent = comment.content;

        // 댓글 작성 시각
        var commentTimestamp = document.createElement('div');
        commentTimestamp.classList.add('comment-createdat');

        var date = new Date(comment.created_at);
        var formattedDate = date.toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
        commentTimestamp.textContent = '작성 시각: ' + formattedDate;

        // 댓글 좋아요
        var commentLike = document.createElement('a');
        commentLike.classList.add('comment-like');
        commentLike.setAttribute('id', comment.id);
        commentLike.textContent = comment.like.length;


        commentBox.appendChild(commentAuthor);
        commentBox.appendChild(commentContent);
        commentBox.appendChild(commentTimestamp);
        commentBox.appendChild(commentLike);
        commentList.appendChild(commentBox);
    }

    function showMessage(message) {
        var messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.classList.add('message');

        // 메시지를 표시할 DOM 엘리먼트에 추가
        var messagesContainer = document.querySelector('.messages-container');
        messagesContainer.appendChild(messageElement);
    }

    function likeComments() {
        var commentElements = document.querySelectorAll('.comment-box');

        commentElements.forEach(function (commentElement) {
            var likeButton = commentElement.querySelector('.comment-like');
            var commentId = likeButton.getAttribute('id');

            likeButton.addEventListener('click', function () {
                fetch(`/api/comment/${commentId}/like/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                })
                .then(function (response) {
                    if (response.status === 201) {
                        return response.json();
                    } else {
                        console.error('댓글 추천 또는 취소 실패');
                        return null;
                    }
                })
                .then(function (data) {
                    var message = data.message;

                    showMessage(message);
                })
                .catch(function (error) {
                    console.error(error);
                })
            })
        })
    }

    fetchComments();
});
