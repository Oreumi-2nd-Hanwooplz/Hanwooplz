document.addEventListener("DOMContentLoaded", function () {
    var commentText = document.getElementById("comment-input");
    var submitButton = document.getElementById("comment-submit-button");
    var csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    // 댓글 불러오기
    function fetchComments() {
        fetch(`/api/post/${postId}/comments/`)
            .then(function (response) {
                return response.json();
            })
            .then(function (comments) {
                var commentList = document.querySelector(".comment-list");
                commentList.innerHTML = "";
                comments.forEach(function (comment) {
                    var commentBox = document.createElement("div");
                    commentBox.classList.add("comment-box");

                    // 댓글 작성자
                    var commentAuthor = document.createElement("div");
                    commentAuthor.classList.add("comment-author");
                    commentAuthor.textContent = comment.author;

                    // 댓글 내용
                    var commentContent = document.createElement("div");
                    commentContent.classList.add("comment-content");
                    commentContent.textContent = comment.content;

                    // 댓글 작성 시각
                    var commentTimestamp = document.createElement("div");
                    commentTimestamp.classList.add("comment-createdat");

                    var date = new Date(comment.created_at);
                    var formattedDate = date.toLocaleString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
                    commentTimestamp.textContent = formattedDate;

                    // 댓글 좋아요 + 삭제
                    var commentBottomWrapper = document.createElement("div");
                    commentBottomWrapper.classList.add("comment-bottom-wrapper");

                    // 댓글 좋아요
                    var commentLike = document.createElement("a");
                    commentLike.classList.add("comment-like");
                    commentLike.setAttribute("id", comment.id);
                    commentLike.textContent = "👍 " + comment.like.length;
                    commentLike.addEventListener("click", function () {
                        upvoteComment(comment.id);
                    })
                    
                    commentBottomWrapper.appendChild(commentLike);
                    commentBox.appendChild(commentAuthor);
                    commentBox.appendChild(commentTimestamp);
                    commentBox.appendChild(commentContent);
                    commentBox.appendChild(commentBottomWrapper);
                    commentList.appendChild(commentBox);

                    // 댓글 삭제
                    if (currentUser === comment.author) {
                        var commentDelete = document.createElement("a");
                        commentDelete.classList.add("comment-delete");
                        commentDelete.textContent = "삭제";
                        commentDelete.addEventListener("click", function () {
                            var deleteConfirmed = confirm("댓글을 삭제하시겠습니까?");
                            if (deleteConfirmed) {
                                deleteComment(comment.id);
                            }
                        })
                        commentBottomWrapper.appendChild(commentDelete);
                    }
                    
                });
            })
            .catch(function (error) {
                alert("댓글을 가져오는 데 실패했습니다.");
            });
    }

    // 댓글 등록
    submitButton.addEventListener("click", function () {
        var commentData = {
            content: commentText.value
        };

        fetch(`/api/post/${postId}/comments/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(commentData),
        })
            .then(function (response) {
                if (response.status === 201) {
                    commentText.value = "";
                    fetchComments();
                } else {
                    alert("댓글 작성에 실패했습니다.");
                }
            });
    });

    // 댓글 추천
    function upvoteComment(commentId) {
        fetch(`/api/comment/${commentId}/like/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
        })
            .then(function (response) {
                if (response.status === 200) {
                    return response.json();
                } else {
                    console.error("댓글 추천 또는 취소 실패");
                    return null;
                }
            })
            .then(function (data) {
                var message = data.message;
                var data = data.comment_data;

                var commentLike = document.getElementById(`${commentId}`);
                commentLike.textContent = data.like.length;

                if (message) {
                    alert(message);
                }
            })
            .catch(function (error) {
                console.error(error);
            })
    }

    // 댓글 삭제
    function deleteComment(commentId) {
        fetch(`/api/comments/${commentId}/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
        })
            .then(function (response) {
                if (response.status === 204) {
                    commentText.value = "";
                    alert("댓글이 삭제되었습니다.")
                    return fetchComments();
                } else if (response.status === 404) {
                    alert("존재하지 않는 댓글입니다.")
                } else {
                    alert("댓글 삭제에 실패했습니다.");
                }
            })
            .catch(function (error) {
                console.error(error);
            });
    }

    fetchComments();
});
