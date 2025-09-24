# nav-site
导航网站
[index.html.html](https://github.com/user-attachments/files/22518646/index.html.html)
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>王安全导航网</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f3fbff;
      padding: 40px;
    }
    .container {
      max-width: 880px;
      margin: auto;
      background: #fff;
      padding: 28px;
      border-radius: 12px;
      box-shadow: 0 8px 30px rgba(10,20,30,0.08);
    }
    h1 {
      text-align: center;
    }
    #search, #nameInput, #urlInput {
      width: 100%;
      padding: 10px;
      margin: 6px 0;
      border: 1px solid #ccc;
      border-radius: 6px;
      box-sizing: border-box;
    }
    ul { list-style: none; padding: 0; }
    li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px;
      border-bottom: 1px solid #eee;
    }
    a { color: #0b79d0; text-decoration: none; }
    .btn {
      padding: 6px 12px;
      margin-left: 4px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
    }
    .btn-edit { background: #f0ad4e; color: white; }
    .btn-delete { background: #d9534f; color: white; }
    .btn-add { background: #0b79d0; color: white; margin-top: 10px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>王安全导航网</h1>
    <!-- 搜索框 -->
    <input id="search" placeholder="搜索关键词（例如：B站）">

    <!-- 链接列表 -->
    <ul id="links"></ul>

    <hr>

    <!-- 新增/修改输入框 -->
    <input id="nameInput" placeholder="网站名称">
    <input id="urlInput" placeholder="网址（例如：https://...）">
    <button id="addBtn" class="btn btn-add">添加链接</button>
  </div>

  <script>
    const searchInput = document.getElementById('search');
    const listEl = document.getElementById('links');
    const nameInput = document.getElementById('nameInput');
    const urlInput = document.getElementById('urlInput');
    const addBtn = document.getElementById('addBtn');

    // 从本地存储加载
    let links = JSON.parse(localStorage.getItem('navLinks')) || [
      {name: "B站", url: "https://www.bilibili.com"},
      {name: "Google", url: "https://www.google.com"},
      {name: "GitHub", url: "https://www.github.com"}
    ];

    let editIndex = null; // 当前是否处于编辑状态

    function renderLinks() {
      listEl.innerHTML = '';
      links.forEach((link, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
          <a href="${link.url}" target="_blank">${link.name}</a>
          <div>
            <button class="btn btn-edit" onclick="editLink(${index})">修改</button>
            <button class="btn btn-delete" onclick="deleteLink(${index})">删除</button>
          </div>
        `;
        listEl.appendChild(li);
      });
      saveLinks();
    }

    function saveLinks() {
      localStorage.setItem('navLinks', JSON.stringify(links));
    }

    // 搜索
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase();
      Array.from(listEl.querySelectorAll('li')).forEach(li => {
        li.style.display = li.textContent.toLowerCase().includes(q) ? '' : 'none';
      });
    });

    // 添加或修改
    addBtn.addEventListener('click', () => {
      const name = nameInput.value.trim();
      const url = urlInput.value.trim();
      if (!name || !url) {
        alert("请输入完整信息！");
        return;
      }

      if (editIndex === null) {
        // 添加模式
        links.push({name, url});
      } else {
        // 修改模式
        links[editIndex] = {name, url};
        editIndex = null;
        addBtn.textContent = "添加链接";
      }

      nameInput.value = '';
      urlInput.value = '';
      renderLinks();
    });

    // 修改
    window.editLink = (index) => {
      nameInput.value = links[index].name;
      urlInput.value = links[index].url;
      editIndex = index;
      addBtn.textContent = "保存修改";
    }

    // 删除
    window.deleteLink = (index) => {
      if (confirm("确定要删除吗？")) {
        links.splice(index, 1);
        renderLinks();
      }
    }

    // 初始渲染
    renderLinks();
  </script>
</body>
</html>
