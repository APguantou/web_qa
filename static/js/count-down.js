// 倒计时功能实现
document.addEventListener('DOMContentLoaded', function() {
    // 获取左侧倒计时元素
    const leftTitleInput = document.getElementById('left-title');
    const leftDateInput = document.getElementById('left-date');
    const leftTimeInput = document.getElementById('left-time');
    const setLeftBtn = document.getElementById('set-left-countdown');

    // 获取右侧倒计时元素
    const rightTitleInput = document.getElementById('right-title');
    const rightDateInput = document.getElementById('right-date');
    const rightTimeInput = document.getElementById('right-time');
    const setRightBtn = document.getElementById('set-right-countdown');

    // 左侧倒计时显示元素
    const leftDaysEl = document.getElementById('left-days');
    const leftHoursEl = document.getElementById('left-hours');
    const leftMinutesEl = document.getElementById('left-minutes');
    const leftSecondsEl = document.getElementById('left-seconds');

    // 右侧倒计时显示元素
    const rightDaysEl = document.getElementById('right-days');
    const rightHoursEl = document.getElementById('right-hours');
    const rightMinutesEl = document.getElementById('right-minutes');
    const rightSecondsEl = document.getElementById('right-seconds');

    // 左侧倒计时定时器
    let leftInterval = null;

    // 右侧倒计时定时器
    let rightInterval = null;

    // 计算倒计时剩余时间的函数
    function calculateRemaining(endTime) {
        const now = new Date().getTime();
        const distance = endTime - now;

        if (distance <= 0) {
            return { days: 0, hours: 0, minutes: 0, seconds: 0 };
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        return { days, hours, minutes, seconds };
    }

    // 更新左侧倒计时显示
    function updateLeftCountdown() {
        const endTimeStr = localStorage.getItem('left-countdown-end');
        if (!endTimeStr) return;

        const endTime = new Date(endTimeStr).getTime();
        const remaining = calculateRemaining(endTime);

        leftDaysEl.textContent = String(remaining.days).padStart(2, '0');
        leftHoursEl.textContent = String(remaining.hours).padStart(2, '0');
        leftMinutesEl.textContent = String(remaining.minutes).padStart(2, '0');
        leftSecondsEl.textContent = String(remaining.seconds).padStart(2, '0');

        if (remaining.days === 0 && remaining.hours === 0 &&
            remaining.minutes === 0 && remaining.seconds === 0) {
            clearInterval(leftInterval);
            leftInterval = null;
        }
    }

    // 更新右侧倒计时显示
    function updateRightCountdown() {
        const endTimeStr = localStorage.getItem('right-countdown-end');
        if (!endTimeStr) return;

        const endTime = new Date(endTimeStr).getTime();
        const remaining = calculateRemaining(endTime);

        rightDaysEl.textContent = String(remaining.days).padStart(2, '0');
        rightHoursEl.textContent = String(remaining.hours).padStart(2, '0');
        rightMinutesEl.textContent = String(remaining.minutes).padStart(2, '0');
        rightSecondsEl.textContent = String(remaining.seconds).padStart(2, '0');

        if (remaining.days === 0 && remaining.hours === 0 &&
            remaining.minutes === 0 && remaining.seconds === 0) {
            clearInterval(rightInterval);
            rightInterval = null;
        }
    }

    // 设置左侧倒计时
    function setLeftCountdown() {
        const title = leftTitleInput.value.trim();
        const date = leftDateInput.value;
        const time = leftTimeInput.value;

        if (!title || !date || !time) {
            alert('请填写完整的倒计时信息（标题、日期和时间）');
            return;
        }

        // 组合日期和时间
        const dateTimeStr = `${date}T${time}`;
        const endTime = new Date(dateTimeStr);

        if (isNaN(endTime.getTime())) {
            alert('请选择有效的时间');
            return;
        }

        if (endTime <= new Date()) {
            alert('结束时间必须晚于当前时间');
            return;
        }

        // 保存到本地存储
        localStorage.setItem('left-countdown-title', title);
        localStorage.setItem('left-countdown-end', endTime.toISOString());

        // 更新标题
        document.querySelector('#main-block9 .countdown-panel:first-child h3').textContent = title;

        // 清除之前的定时器
        if (leftInterval) {
            clearInterval(leftInterval);
        }

        // 开始新的倒计时
        updateLeftCountdown(); // 立即更新一次
        leftInterval = setInterval(updateLeftCountdown, 1000);
    }

    // 设置右侧倒计时
    function setRightCountdown() {
        const title = rightTitleInput.value.trim();
        const date = rightDateInput.value;
        const time = rightTimeInput.value;

        if (!title || !date || !time) {
            alert('请填写完整的倒计时信息（标题、日期和时间）');
            return;
        }

        // 组合日期和时间
        const dateTimeStr = `${date}T${time}`;
        const endTime = new Date(dateTimeStr);

        if (isNaN(endTime.getTime())) {
            alert('请选择有效的时间');
            return;
        }

        if (endTime <= new Date()) {
            alert('结束时间必须晚于当前时间');
            return;
        }

        // 保存到本地存储
        localStorage.setItem('right-countdown-title', title);
        localStorage.setItem('right-countdown-end', endTime.toISOString());

        // 更新标题
        document.querySelector('#main-block9 .countdown-panel:last-child h3').textContent = title;

        // 清除之前的定时器
        if (rightInterval) {
            clearInterval(rightInterval);
        }

        // 开始新的倒计时
        updateRightCountdown(); // 立即更新一次
        rightInterval = setInterval(updateRightCountdown, 1000);
    }

    // 设置默认左侧倒计时
    function setDefaultLeftCountdown() {
        const defaultTitle = '27研究生倒计时';
        const defaultDate = '2026-12-21';
        const defaultTime = '08:00';

        // 检查是否已有自定义设置
        const existingTitle = localStorage.getItem('left-countdown-title');
        if (existingTitle) return; // 如果已有自定义设置则不覆盖

        // 设置默认值到输入框
        leftTitleInput.value = defaultTitle;
        leftDateInput.value = defaultDate;
        leftTimeInput.value = defaultTime;

        // 组合日期和时间
        const dateTimeStr = `${defaultDate}T${defaultTime}`;
        const endTime = new Date(dateTimeStr);

        // 保存到本地存储
        localStorage.setItem('left-countdown-title', defaultTitle);
        localStorage.setItem('left-countdown-end', endTime.toISOString());

        // 更新标题
        document.querySelector('#main-block9 .countdown-panel:first-child h3').textContent = defaultTitle;

        // 立即更新显示
        updateLeftCountdown();

        // 开始定时器
        if (leftInterval) {
            clearInterval(leftInterval);
        }
        leftInterval = setInterval(updateLeftCountdown, 1000);
    }

    // 绑定按钮事件
    setLeftBtn.addEventListener('click', setLeftCountdown);
    setRightBtn.addEventListener('click', setRightCountdown);

    // 页面加载时恢复之前的倒计时
    window.addEventListener('load', function() {
        // 恢复左侧倒计时
        const leftTitle = localStorage.getItem('left-countdown-title');
        const leftEnd = localStorage.getItem('left-countdown-end');

        if (leftTitle && leftEnd) {
            document.querySelector('#main-block9 .countdown-panel:first-child h3').textContent = leftTitle;
            const endTime = new Date(leftEnd).getTime();
            const now = new Date().getTime();

            if (endTime > now) {
                updateLeftCountdown();
                leftInterval = setInterval(updateLeftCountdown, 1000);
            } else {
                // 时间已过，清除存储并设置默认倒计时
                localStorage.removeItem('left-countdown-title');
                localStorage.removeItem('left-countdown-end');
                setDefaultLeftCountdown();
            }
        } else {
            // 如果没有存储的倒计时，设置默认倒计时
            setDefaultLeftCountdown();
        }

        // 恢复右侧倒计时
        const rightTitle = localStorage.getItem('right-countdown-title');
        const rightEnd = localStorage.getItem('right-countdown-end');

        if (rightTitle && rightEnd) {
            document.querySelector('#main-block9 .countdown-panel:last-child h3').textContent = rightTitle;
            const endTime = new Date(rightEnd).getTime();
            const now = new Date().getTime();

            if (endTime > now) {
                updateRightCountdown();
                rightInterval = setInterval(updateRightCountdown, 1000);
            } else {
                // 时间已过，清除存储
                localStorage.removeItem('right-countdown-title');
                localStorage.removeItem('right-countdown-end');
            }
        }
    });
});
