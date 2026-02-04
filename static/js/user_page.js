// 注销确认功能
// 替换原来的 confirmLogout 函数
function confirmLogout() {
    if (confirm("您确定要注销吗？这将会从数据库中删除您的账户信息。")) {
        // 发送请求到后端执行账户删除操作
        fetch('/auth/delete_account_cgw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin' // 包含cookie
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('账户已成功删除！');
                    window.location.href = '/'; // 重定向到首页
                } else {
                    alert('删除失败：' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('注销过程中出现错误。');
            });
    }
}

function togglePointsDetail() {
    const detailElement = document.getElementById('points-detail');
    if (detailElement.style.display === 'none' || detailElement.style.display === '') {
        // 展开
        detailElement.style.display = 'block';
        detailElement.style.opacity = '0';
        detailElement.style.maxHeight = '0';
        setTimeout(() => {
            detailElement.style.transition = 'opacity 0.3s ease, max-height 0.3s ease';
            detailElement.style.opacity = '1';
            detailElement.style.maxHeight = '200px'; // 设置最大高度
        }, 10);
    } else {
        // 收起
        detailElement.style.transition = 'opacity 0.3s ease, max-height 0.3s ease';
        detailElement.style.opacity = '0';
        detailElement.style.maxHeight = '0';
        setTimeout(() => {
            detailElement.style.display = 'none';
        }, 300);
    }
}

function showTab(tabName) {
    // 隐藏所有 tab 内容
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // 移除所有按钮的 active 类
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.classList.remove('active');
    });

    // 显示当前 tab 内容
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // 给当前按钮添加 active 类
    event.target.classList.add('active');
}

const baseUrl = "{{ url_for('auth.delete_question', question_id=0) }}".replace('/0', '');

function deletePost(question_id) {
    if (confirm(`您确定要删除这篇帖子吗？此操作不可撤销。`)) {
        $.ajax({
            url: `${baseUrl}/${question_id}`, // 确保路径中只有一个斜杠
            type: 'DELETE',
            success: function (data) {
                if (data.success) {
                    alert('帖子删除成功！');
                    location.reload();
                } else {
                    alert('删除失败：' + data.message);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('删除过程中出现错误。');
            }
        });
    }
}