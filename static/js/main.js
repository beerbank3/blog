function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 페이지 로딩이 완료되면 버튼에 이벤트 리스너를 등록
window.onload = function() {
    const topButton = document.querySelector('.top-button');
    topButton.addEventListener('click', scrollToTop);
};