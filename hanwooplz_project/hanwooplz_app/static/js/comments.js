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
                var commentList = document.querySelector('.comment-container');
                //commentList.innerHTML = '';
                comments.forEach(function (comment) {
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

                    commentBox.appendChild(commentAuthor);
                    commentBox.appendChild(commentContent);
                    commentList.appendChild(commentBox);
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
                    fetchComments();
                } else {
                    alert('댓글 작성에 실패했습니다.');
                }
            });
    });

    fetchComments();
});
