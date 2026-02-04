document.getElementById('forget-pwd-form').addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止默认提交行为

    const email = document.getElementById('email-input').value;
    const email_captcha = document.querySelector('input[name="email_captcha"]').value;
    const new_password = document.querySelector('input[name="new_password"]').value;

    // 校验字段是否为空
    if (!email || !email_captcha || !new_password) {
        alert("请填写所有必填项");
        return;
    }

    // 发送请求到后端重置密码
    fetch('/auth/reset_pwd_cgw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${encodeURIComponent(email)}&email_captcha=${encodeURIComponent(email_captcha)}&new_password=${encodeURIComponent(new_password)}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("密码重置成功！");
                window.location.href = "/auth/login_cgw"; // 跳转到登录页面
            } else {
                alert(`重置失败：${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("网络错误，请稍后再试");
        });
});
document.getElementById('send-captcha-btn').addEventListener('click', function () {
    const email = document.getElementById('email-input').value;
    if (!email) {
        alert("请输入邮箱地址");
        return;
    }

    fetch('/auth/send_email_captcha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${encodeURIComponent(email)}`
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert("验证码已发送至您的邮箱，请查收");
            } else {
                alert(`发送失败：${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("网络错误，请稍后再试");
        });
});