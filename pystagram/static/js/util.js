$(document).ready(function () {

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#scroll-to-top').fadeIn();
        } else {
            $('#scroll-to-top').fadeOut();
        }
    });

        $('#scroll-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 500);
        return false;
    });

    //댓글 버튼 각 포스트 아이디별 폼 불러오기
    $(".comment_form_btn").click(function () {
        // data-post-id를 통해 post.id 값을 가져오기
        const postId = $(this).data("post-id");


        // alert("postId " + postId)
        // 가져온 post.id를 사용하여 원하는 동작 수행
        toggleCommentForm(postId)
        commentHandleCharacterCount(postId)

        // 글자수 제한하는 함수

    });

    //메세지 보내기 버튼 각 포스트 아이디별 모달폼창 불러오기
    $(".send_message_form_btn").click(function () {
        // data-post-id를 통해 post.id 값을 가져오기
        const postId = $(this).data("post-id");


        // alert("postId " + postId)
        // console.log("postId " + postId)
        // 가져온 post.id를 사용하여 원하는 동작 수행
        // sendMessageToggleModalForm(postId)
        toggleSendMessageForm(postId)
        messageHandleCharacterCount(postId)

    });


    // 메세지 글자수 제한
    function messageHandleCharacterCount(postId) {
            // Get the textarea element, character count paragraph, and the button
            const textarea = document.getElementById(`message_content_${postId}`);
            const charCount = document.getElementById(`messageCharCount_${postId}`);
            const myButton = document.getElementById(`message_send_btn_${postId}`);

            // Set the maximum character limit
            const maxChars = 300;

            // Add an input event listener to the textarea
            textarea.addEventListener('input', function() {
                const currentChars = textarea.value.length;
                const remainingChars = maxChars - currentChars;

                // Update the character count display
                charCount.textContent = `남은 글자수 : ${remainingChars}`;

                // Limit the input to the maximum characters
                if (currentChars > maxChars) {
                    textarea.value = textarea.value.substring(0, maxChars);
                    charCount.textContent = '최대 글자수를 초과 했어요.';
                }

                // Disable the button when the character count exceeds the limit
                myButton.disabled = currentChars > maxChars;
            });
        }
    
    // 댓글 글자수 제한
    function commentHandleCharacterCount(postId) {
            // Get the textarea element, character count paragraph, and the button
            const textarea = document.getElementById(`comment_content_${postId}`);
            const charCount = document.getElementById(`charCount_${postId}`);
            const myButton = document.getElementById(`comment_send_btn_${postId}`);

            // Set the maximum character limit
            const maxChars = 200;

            // Add an input event listener to the textarea
            textarea.addEventListener('input', function() {
                const currentChars = textarea.value.length;
                const remainingChars = maxChars - currentChars;

                // Update the character count display
                charCount.textContent = `남은 글자수 : ${remainingChars}`;

                // Limit the input to the maximum characters
                if (currentChars > maxChars) {
                    textarea.value = textarea.value.substring(0, maxChars);
                    charCount.textContent = '최대 글자수를 초과 했어요.';
                }

                // Disable the button when the character count exceeds the limit
                myButton.disabled = currentChars > maxChars;
            });
        }


     // 메시지 폼 모달 기능
    function sendMessageToggleModalForm(postId) {
        const openModalBtn = document.getElementById(`send_message_form_btn_${postId}`);
        const closeModalBtn = document.getElementById('closeModalBtn');
        const modal = document.getElementById('myModal');
        const messageForm = document.getElementById('messageForm');


        openModalBtn.addEventListener('click', function () {
            modal.style.display = 'block';
        });

        closeModalBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });

        messageForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const messageTitle = document.getElementById('messageTitle').value;
            const messageContent = document.getElementById('messageContent').value;

            // 여기에서 쪽지를 보내는 동작을 수행합니다.
            // 예: 서버로 데이터 전송 또는 다른 원하는 동작 수행

            alert(`제목: ${messageTitle}\n내용: ${messageContent}`);
            modal.style.display = 'none';
        });

    }

    // 댓글 폼 토글 기능
    function toggleCommentForm(postId) {
        const showFormBtn = document.getElementById(`comment_form_btn_${postId}`);
        const commentForm = document.getElementById(`comment_form_${postId}`);


        const computedStyle = getComputedStyle(commentForm);

        // console.log(("computedStyle.display : " + computedStyle.display))

        if (computedStyle.display === 'none') {
            commentForm.style.display = 'flex';

        } else {
            commentForm.style.display = 'none';
        }

    }

      // 쪽지 보내기 폼 토글 기능
    function toggleSendMessageForm(postId) {
        const showFormBtn = document.getElementById(`send_message_form_btn_${postId}`);
        const commentForm = document.getElementById(`send_message_form_${postId}`);


        const computedStyle = getComputedStyle(commentForm);

        // console.log(("computedStyle.display : " + computedStyle.display))

        if (computedStyle.display === 'none') {
            commentForm.style.display = 'flex';

        } else {
            commentForm.style.display = 'none';
        }

    }

})




