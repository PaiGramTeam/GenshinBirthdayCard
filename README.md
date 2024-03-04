# Genshin Birthday Card

本项目存档了 留影叙佳期 活动的所有生日卡片. (2022-03 ~ 2024-02)

## files 项目结构

```
.
├── aether （男主）
│   ├── 2022
│   │   ├── 3
│   │   │   ├── 七七.jpg
...
├── lumine （女主）
│   ├── 2022
│   │   ├── 3
│   │   │   ├── 七七.jpg
...
├── resource （galgame 资源）
│   ├── bg （背景）
│   ├── chara （角色）
...
```

## 环境变量

```
COOKIES=  (cookies)
GENSHIN_PLAYER_ID=  (genshin uid)
GENSHIN_GENDER_BOY=true  (是否男主)
```

## 使用方法

```bash
# 安装依赖
pip install -r requirements.txt
# 运行
python main.py
```
