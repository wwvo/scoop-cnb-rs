# scoop-cnb-cli

[cnb CLI](https://cnb.cool/wwvo/cnb-cli/cnb) 的 [Scoop](https://scoop.sh) Bucket。

cnb 是一个非官方的 [CNB (cnb.cool)](https://cnb.cool) 命令行工具。

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

安装后可启用 PowerShell 命令行补全：

```pwsh
# 添加到 PowerShell 配置文件（永久生效）
cnb completion powershell >> $PROFILE

# 或仅在当前会话中启用
cnb completion powershell | Out-String | Invoke-Expression
```

重新打开终端后即可使用 `Tab` 键补全 cnb 的子命令和参数。

## 相关链接

- [CNB CLI 文档](https://cnb.wwvo.fun)
- [CNB CLI 源码](https://cnb.cool/wwvo/cnb-cli/cnb)
