from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_implement_command_requires_fine_grained_git_checkpoints():
    content = (ROOT / "templates" / "commands" / "implement.md").read_text(encoding="utf-8")

    assert "Git checkpoint 策略" in content
    assert "不得" in content and "巨大提交" in content
    assert "git push" in content and "用户明确要求" in content
    assert "只 stage 当前任务组相关文件" in content


def test_tasks_template_exposes_checkpoint_boundaries():
    content = (ROOT / "templates" / "tasks-template.md").read_text(encoding="utf-8")

    assert "Git checkpoint" in content
    assert "每完成一个可独立验证的阶段、用户故事或任务组" in content
    assert "默认只创建本地 commit" in content


def test_constitution_template_mentions_checkpoint_governance():
    content = (ROOT / "templates" / "constitution-template.md").read_text(encoding="utf-8")

    assert "Git checkpoint policy" in content
    assert "多步骤需求不得以一个巨大最终提交收尾" in content
