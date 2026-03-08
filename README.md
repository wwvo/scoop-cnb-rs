# scoop-cnb-cli

[CNB CLI](https://cnb.cool/wwvo/cnb-cli/cnb) 的 [Scoop](https://scoop.sh) Bucket。

CNB CLI 是一个非官方的 [CNB (cnb.cool)](https://cnb.cool) 命令行工具。

## 安装

```pwsh
scoop bucket add cnb-cli https://cnb.cool/wwvo/cnb-cli/scoop-cnb-cli.git
scoop install cnb-cli/cnb
```

## 更新

```pwsh
scoop update cnb
```

## 终端补全

安装后可启用 PowerShell 命令行补全。在 PowerShell 中执行：

```pwsh
# 启用菜单补全（Tab 显示候选列表和描述）
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

# 加载 cnb 补全脚本
cnb completion powershell | Out-String | Invoke-Expression
```

若要每次启动自动生效，将上述内容写入 PowerShell 配置文件：

```pwsh
# 查看配置文件路径
$PROFILE

# 编辑配置文件（如果不存在会自动创建）
if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Force }
notepad $PROFILE
```

## 相关链接

- [CNB CLI 文档](https://cnb.wwvo.fun)
- [CNB CLI 源码](https://cnb.cool/wwvo/cnb-cli/cnb)
