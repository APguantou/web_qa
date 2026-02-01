// GPA计算器功能实现
document.addEventListener('DOMContentLoaded', function() {
    // 获取表单元素
    const form = document.getElementById('course-form');
    const semesterSelect = document.getElementById('semester-select');
    const courseNameInput = document.getElementById('course-name');
    const courseCreditInput = document.getElementById('course-credit');
    const courseScoreInput = document.getElementById('course-score');
    const submitBtn = document.getElementById('submit-btn');
    const coursesTbody = document.getElementById('courses-tbody');
    const avgGpaValue = document.getElementById('avg-gpa-value');
    const courseOptionsList = document.getElementById('course-options');

    // 从localStorage加载已保存的课程数据
    let courses = JSON.parse(localStorage.getItem('courses')) || [];

    // 课程计划数据
    const coursePlan = {
        courses: [
            {
                "课程类别": "通识教育必修",
                "课程名称": "形势与政策",
                "开课学期": [5, 6, 7, 8],
                "学分": 0.25
            },
            {
                "课程类别": "通识教育必修",
                "课程名称": "劳动教育与实践",
                "开课学期": [ 6, 7],
                "学分": 0.5
            },
            {
                "课程类别": "学科基础课",
                "课程名称": "审计学",
                "开课学期": [5],
                "学分": 2
            },
            {
                "课程类别": "学科基础课",
                "课程名称": "程序设计与数据结构",
                "开课学期": [5],
                "学分": 4
            },
            {
                "课程类别": "学科基础课",
                "课程名称": "计算机组成原理",
                "开课学期": [5],
                "学分": 4
            },
            {
                "课程类别": "学科基础课",
                "课程名称": "数字社会学",
                "开课学期": [6],
                "学分": 2
            },
            {
                "课程类别": "专业主干课",
                "课程名称": "计算机网络",
                "开课学期": [5],
                "学分": 4
            },
            {
                "课程类别": "专业主干课",
                "课程名称": "python程序设计",
                "开课学期": [6],
                "学分": 3
            },
            {
                "课程类别": "专业主干课",
                "课程名称": "数据库原理及应用",
                "开课学期": [6],
                "学分": 4
            },
            {
                "课程类别": "专业主干课",
                "课程名称": "信息系统安全",
                "开课学期": [5],
                "学分": 3
            },
            {
                "课程类别": "专业主干课",
                "课程名称": "操作系统原理",
                "开课学期": [6],
                "学分": 3
            },
            {
                "课程类别": "专业主干课",
                "课程名称": "web开发技术",
                "开课学期": [6],
                "学分": 2
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "面向对象程序设计",
                "开课学期": [6],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "软件工程",
                "开课学期": [6],
                "学分": 4
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "网络攻击与防护",
                "开课学期": [5],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "电子取证技术",
                "开课学期": [6],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "网络编程技术",
                "开课学期": [7],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "云计算与边缘计算",
                "开课学期": [5],
                "学分": 1
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "Linux系统管理及服务器管理",
                "开课学期": [6],
                "学分": 2
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "互联网应用开发",
                "开课学期": [6],
                "学分": 4
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "人工智能",
                "开课学期": [6],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "大数据技术",
                "开课学期": [6],
                "学分": 1
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "软件架构设计",
                "开课学期": [7],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "未来网络技术",
                "开课学期": [7],
                "学分": 1
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "深度学习",
                "开课学期": [7],
                "学分": 3
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "Oracle数据库技术",
                "开课学期": [7],
                "学分": 2
            },
            {
                "课程类别": "专业方向课",
                "课程名称": "新技术综述",
                "开课学期": [8],
                "学分": 1
            },
            {
                "课程类别": "实训课",
                "课程名称": "基础编程综合实训",
                "开课学期": [5],
                "学分": 1
            },
            {
                "课程类别": "实训课",
                "课程名称": "信息系统开发实训",
                "开课学期": [7],
                "学分": 1
            },
            {
                "课程类别": "创新创业与社会实践",
                "课程名称": "就业指导",
                "开课学期": [7],
                "学分": 0.25
            },
            {
                "课程类别": "创新创业与社会实践",
                "课程名称": "职业生涯规划",
                "开课学期": [5, 6],
                "学分": 0.25
            },
            {
                "课程类别": "创新创业与社会实践",
                "课程名称": "暑期社会实践活动",
                "开课学期": [6],
                "学分": 0.5
            },
            {
                "课程类别": "创新创业与社会实践",
                "课程名称": "创新创业指导",
                "开课学期": [5, 6],
                "学分": 0.25
            }
        ]
    };

    // 计算课程绩点的函数 (成绩-50)/10，保留一位小数
    function calculateGPA(score) {
        if (score < 60) return 0.0; // 不及格绩点为0
        const gpa = (score - 50) / 10;
        return parseFloat(gpa.toFixed(1));
    }

    // 计算平均绩点的函数 (各科绩点*学分之和) / 学分总和
    function calculateAverageGPA(coursesList) {
        if (coursesList.length === 0) return 0.0;

        let totalWeightedGPA = 0;
        let totalCredits = 0;

        for (const course of coursesList) {
            totalWeightedGPA += course.gpa * course.credit;
            totalCredits += course.credit;
        }

        if (totalCredits === 0) return 0.0;

        const average = totalWeightedGPA / totalCredits;
        return parseFloat(average.toFixed(1));
    }

    // 根据学期筛选课程
    function filterCoursesBySemester(semester) {
        if (!semester) {
            return coursePlan.courses;
        }
        return coursePlan.courses.filter(course => course['开课学期'].includes(parseInt(semester)));
    }

    // 填充课程选项到datalist
    function populateCourseOptions(semester) {
        courseOptionsList.innerHTML = '';
        const filteredCourses = filterCoursesBySemester(semester);

        filteredCourses.forEach(course => {
            const option = document.createElement('option');
            option.value = course['课程名称'];
            option.dataset.credit = course['学分'];
            courseOptionsList.appendChild(option);
        });
    }

    // 当选择课程名称时自动填写学分
    courseNameInput.addEventListener('change', function() {
        const selectedOption = Array.from(courseOptionsList.options).find(
            option => option.value === this.value
        );
        if (selectedOption && selectedOption.dataset.credit) {
            courseCreditInput.value = selectedOption.dataset.credit;
        } else {
            courseCreditInput.value = '';
        }
    });

    // 显示课程列表
    function displayCourses() {
        // 清空现有列表
        coursesTbody.innerHTML = '';

        // 添加每门课程到表格
        courses.forEach(course => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${course.name}</td>
                <td>${course.credit}</td>
                <td>${course.score}</td>
                <td>${course.gpa}</td>
            `;

            coursesTbody.appendChild(row);
        });

        // 更新平均绩点显示
        const avgGpa = calculateAverageGPA(courses);
        avgGpaValue.textContent = avgGpa;

        // 保存到localStorage
        localStorage.setItem('courses', JSON.stringify(courses));
    }
    // 添加清空功能
function addClearFunctionality() {
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.id = 'clear-btn';
    clearBtn.textContent = '清空所有课程';
    clearBtn.style.marginTop = '10px';
    clearBtn.style.backgroundColor = '#f44336';
    clearBtn.style.color = 'white';
    clearBtn.style.padding = '10px 20px';
    clearBtn.style.border = 'none';
    clearBtn.style.borderRadius = '4px';
    clearBtn.style.cursor = 'pointer';

    clearBtn.addEventListener('click', function() {
        if(confirm('确定要清空所有课程吗？此操作不可恢复。')) {
            courses = []; // 清空课程数组
            localStorage.removeItem('courses'); // 删除本地存储
            displayCourses(); // 刷新显示
        }
    });

    // 在提交按钮后添加清空按钮
    submitBtn.parentNode.insertBefore(clearBtn, submitBtn.nextSibling);
}

// 在初始化完成后调用
addClearFunctionality();

    // 表单提交事件处理
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // 阻止默认提交行为

        // 获取输入值
        const courseName = courseNameInput.value.trim();
        let courseCredit = parseFloat(courseCreditInput.value);
        const courseScore = parseInt(courseScoreInput.value);

        // 如果没有手动输入学分，尝试从课程计划中获取
        if (isNaN(courseCredit)) {
            const courseInPlan = coursePlan.courses.find(course => course['课程名称'] === courseName);
            if (courseInPlan) {
                courseCredit = courseInPlan['学分'];
            }
        }

        // 验证输入
        if (!courseName || isNaN(courseCredit) || isNaN(courseScore) ||
            courseScore < 0 || courseScore > 100 || courseCredit <= 0) {
            alert('请输入有效的课程信息（成绩应在0-100之间，学分应大于0）');
            return;
        }

        // 计算绩点
        const gpa = calculateGPA(courseScore);

        // 创建课程对象
        const newCourse = {
            name: courseName,
            credit: courseCredit,
            score: courseScore,
            gpa: gpa
        };

        // 添加到课程数组
        courses.push(newCourse);

        // 显示更新后的课程列表
        displayCourses();

        // 清空表单
        form.reset();
        courseCreditInput.value = '';
    });

    // 为输入框绑定Enter键事件
    courseScoreInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // 阻止默认换行行为
            form.dispatchEvent(new Event('submit')); // 触发表单提交

            // 提交后将焦点返回到课程成绩输入框
            setTimeout(() => {
                courseScoreInput.focus();
            }, 10);
        }
    });

    // 学期选择改变事件
    semesterSelect.addEventListener('change', function() {
        populateCourseOptions(this.value);
    });

    // 初始化显示
    populateCourseOptions('');
    displayCourses();
});
