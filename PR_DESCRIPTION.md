# Bug Fix: Correct enum comparison logic in action connectors

## 问题描述
发现并修复了OM1库中多个action connector的逻辑错误。这些connector错误地将枚举对象与字符串字面量进行比较，导致动作命令永远无法正确匹配。

## 错误示例
```python
# 错误的写法：
if output_interface.action == "walk":  # MovementAction.WALK != "walk"
    new_msg["move"] = "walk"

# 正确的写法：
if output_interface.action == MovementAction.WALK:
    new_msg["move"] = "walk"
```

## 修复的文件
- `src/actions/move/connector/ros2.py` - 修复MovementAction枚举比较
- `src/actions/arm_g1/connector/unitree_sdk.py` - 修复ArmAction枚举比较
- `src/actions/face/connector/ros2.py` - 修复FaceAction枚举比较
- `src/actions/face/connector/avatar.py` - 修复FaceAction枚举比较

## 具体更改
1. 添加了正确的枚举导入到每个connector文件
2. 将所有字符串比较替换为枚举比较
3. 保持了与现有字符串值消息的向后兼容性
4. 修复了动作命令无法正确执行的逻辑错误

## 影响范围
这个修复影响所有使用以下动作的OM1代理：
- 移动动作 (站立、坐下、跳舞、行走等)
- 手臂动作 (挥手、鼓掌、握手等)
- 面部表情动作 (开心、悲伤、好奇等)

## 测试建议
建议测试以下场景：
1. 代理响应移动指令
2. G1机器人执行手臂动作
3. 代理显示面部表情
4. 通过WebSim验证动作执行

此修复确保了动作命令能够正确匹配和执行。