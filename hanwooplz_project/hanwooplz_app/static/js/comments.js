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
        commentTimestamp.classList.add('comment-timestamp');

        var date = new Date(comment.created_at);
        var formattedDate = date.toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
        commentTimestamp.textContent = '작성 시각: ' + formattedDate;

        // 댓글 좋아요
        var commentLike = document.createElement('a');
        commentLike.classList.add('comment-like');
        commentLike.textContent = comment.like.length;


        commentBox.appendChild(commentAuthor);
        commentBox.appendChild(commentContent);
        commentBox.appendChild(commentTimestamp);
        commentBox.appendChild(commentLike);
        commentList.appendChild(commentBox);
    }

    fetchComments();
});
