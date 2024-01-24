document.addEventListener("DOMContentLoaded", function() {
    var inputElement = document.getElementById("id_images");
    var uploadButton = document.getElementById("uploadButton");
    var maxFileCount = 10;  // 허용하는 최대 파일 개수

    inputElement.addEventListener("change", function() {
        var selectedFiles = inputElement.files;
        if (selectedFiles.length > maxFileCount) {
            alert("이미지는 최대 " + maxFileCount + "장까지 선택할 수 있습니다.");
            inputElement.value = "";  // 파일 선택을 취소합니다.
        }
    });

    uploadButton.addEventListener("click", function() {
        // 파일 업로드를 처리하는 코드를 추가하세요.
        // 이 코드는 선택한 파일의 개수가 허용된 최대 개수보다 적을 때만 실행됩니다.
    });
});