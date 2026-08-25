# X 博主动态墙 · 每日自动更新

把关注博主的 X 最新推文，每天自动同步到一个网页，并可嵌入你的 ChatGPT 网站。

**成本：0 元**（不需要 X 官方 API，只用 GitHub 免费服务）

---

## 项目文件说明

| 文件 | 作用 |
|------|------|
| `fetch_x.py` | 抓取脚本：用登录 Cookie 抓取所有博主的最新推文 |
| `followed.txt` | 博主名单（一行一个：用户名 空格 显示名，`#` 开头为注释） |
| `index.html` | 展示页：博主动态墙（可筛选博主、按点赞/时间排序） |
| `data.json` | 每次抓取自动生成的推文数据（不用手动管） |
| `.github/workflows/daily.yml` | 每天自动运行的定时任务 |

---

## 部署步骤（约 10 分钟）

### 第 1 步：创建 GitHub 仓库并上传文件

1. 登录 GitHub → 右上角 **+** → **New repository**
2. 仓库名填 `x-feed-site`（可自定）→ 选 **Public** → **Create repository**
3. 进入仓库后，点 **Add file → Upload files**，把本项目所有文件拖进去上传（含 `index.html`、`fetch_x.py`、`followed.txt`、`.github` 文件夹）
4. 点 **Commit changes** 提交

> 上传时 `.github` 文件夹要保持结构：`.github/workflows/daily.yml`

### 第 2 步：配置登录 Cookie（仓库 Secrets）

1. 进入仓库 → **Settings** → 左侧 **Secrets and variables** → **Actions**
2. 点 **New repository secret**，添加两个：
   - Name: `X_AUTH_TOKEN`，Value: 你的 X 账号 auth_token Cookie 值
   - Name: `X_CT0`，Value: 你的 X 账号 ct0 Cookie 值
3. 这两个值怎么取：
   - 浏览器登录 x.com → 按 `F12` → **Application** 面板 → 左侧 **Cookies** → `https://x.com`
   - 点选 `auth_token` 那行，右侧显示完整值，复制
   - 点选 `ct0` 那行，同样复制完整值

> Cookie 存在 GitHub 的 Secret 里，加密存储，仓库代码和网页都看不到明文。

### 第 3 步：开启 GitHub Pages

1. 仓库 → **Settings** → 左侧 **Pages**
2. **Build and deployment** 的 Source 选 **GitHub Actions**
3. 保存

### 第 4 步：运行一次，验证效果

1. 进入仓库 **Actions** 页
2. 左侧选中 **每日抓取博主推文并更新页面**
3. 点 **Run workflow → Run workflow**
4. 等待约 1-2 分钟跑完（绿色 ✅）
5. 跑完后访问你的页面地址：
   `https://你的用户名.github.io/仓库名/`
   例如：`https://ktingshu.github.io/x-feed-site/`

---

## 自动更新说明

- 每天 **北京时间 08:30** 自动抓取一次全部博主的最新推文并更新网页
- 想改时间：编辑 `.github/workflows/daily.yml` 里的 `cron: '30 0 * * *'`（`0 * * *` 是 UTC 时间，UTC+8 = 北京时间）
- 想改博主名单：编辑 `followed.txt`，增删行即可，下次运行自动生效

### Cookie 失效了怎么办

如果 Actions 运行报错（登录失效），重新取一次 Cookie 更新到 Secret 即可：

Settings → Secrets and variables → Actions → 点 `X_AUTH_TOKEN` / `X_CT0` 的编辑 → 粘贴新值 → 保存

---

## 把动态墙加进你的 ChatGPT 网站

在你的 ChatGPT 网站对话里，让 ChatGPT 在网站加一个"博主动态"入口：

> 在网站导航加一个"博主动态"栏目，放一个按钮/卡片，点击跳转到：`https://你的用户名.github.io/仓库名/`

如果想要更沉浸（不跳转页面），也可以让 ChatGPT 用 iframe 把动态墙嵌进网站页面里。

---

## 隐私与风险提示

- 本项目用你的 X 登录态读取公开内容，属于平台条款的灰色地带（只读、低风险），但理论上有账号被风控的可能，请知情使用
- Cookie 只用于读取公开推文，不会修改你的账号任何内容
