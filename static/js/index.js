// 页面加载完成后执行初始化操作
document.addEventListener('DOMContentLoaded', function () {
    // 获取导航栏元素及其原始位置
    const navbar = document.querySelector('.navbar');
    const originalTop = navbar.offsetTop;
    let isStuck = false; // 标记导航栏是否已固定

    // 处理滚动事件，实现导航栏粘性效果
    function handleScroll() {
        if (window.scrollY > originalTop && !isStuck) {
            // 当滚动超过原始位置时，添加粘性类
            navbar.classList.add('sticky-top');
            isStuck = true;
        } else if (window.scrollY <= originalTop && isStuck) {
            // 当滚动回到原始位置时，移除粘性类
            navbar.classList.remove('sticky-top');
            isStuck = false;
        }
    }

    // 监听滚动事件
    window.addEventListener('scroll', handleScroll);

    // 初始化状态，检查当前是否需要应用粘性效果
    handleScroll();
});

// 异步函数：更新天气信息
async function updateWeather() {
    try {
        // 请求天气API
        const response = await fetch('/api/weather');
        const data = await response.json();

        // 如果没有错误，更新天气信息
        if (!data.error) {
            document.getElementById('weather-info').innerText =
                `${data.city}: ${data.temperature}°C, ${data.description}`;
        } else {
            // 如果有错误，显示默认提示
            document.getElementById('weather-info').innerText = "天气服务暂时不可用";
        }
    } catch (error) {
        // 捕获异常并输出错误日志
        console.error("获取天气失败:", error);
        document.getElementById('weather-info').innerText = "天气服务暂时不可用";
    }
}

// 页面加载完成后立即调用一次天气更新
document.addEventListener('DOMContentLoaded', updateWeather);

// 设置定时器，每小时自动更新一次天气
setInterval(updateWeather, 3600000);
