    document.addEventListener('DOMContentLoaded', function () {
        const navbar = document.querySelector('.navbar');
        const originalTop = navbar.offsetTop;
        let isStuck = false;

        function handleScroll() {
            if (window.scrollY > originalTop && !isStuck) {
                navbar.classList.add('sticky-top');
                isStuck = true;
            } else if (window.scrollY <= originalTop && isStuck) {
                navbar.classList.remove('sticky-top');
                isStuck = false;
            }
        }

        window.addEventListener('scroll', handleScroll);

        // 初始化状态
        handleScroll();
    });
