#!/usr/bin/env bash
# Sync custom skills to workspace by creating symlinks
#
# Structure:
#   /home/art/projects/skills/shared/    → Both agents
#   /home/art/projects/skills/personal/  → Main agent only
#   /home/art/projects/skills/work/      → Work agent only
#   bundled clawdbot skills             → All agents (lower priority)
#
# Workspaces:
#   /home/art/niemand/skills/       → shared + personal + bundled
#   /home/art/niemand-work/skills/  → shared + work + bundled

set -e

SKILLS_ROOT="/home/art/projects/skills"
BUNDLED_SKILLS="/home/art/.npm-packages/lib/node_modules/clawdbot/skills"
MAIN_WORKSPACE="/home/art/niemand/skills"
WORK_WORKSPACE="/home/art/niemand-work/skills"

link_skills() {
    local target_dir="$1"
    shift
    local source_dirs=("$@")

    mkdir -p "$target_dir"

    # Clear existing symlinks
    find "$target_dir" -maxdepth 1 -type l -delete 2>/dev/null || true

    local count=0
    for src_dir in "${source_dirs[@]}"; do
        [[ -d "$src_dir" ]] || continue
        for skill_path in "$src_dir"/*/SKILL.md; do
            [[ -f "$skill_path" ]] || continue
            skill_dir="$(dirname "$skill_path")"
            skill_name="$(basename "$skill_dir")"
            ln -sfn "$skill_dir" "$target_dir/$skill_name"
            count=$((count + 1))
        done
    done
    echo "$count"
}

echo "=== Syncing Main Agent (shared + personal + bundled) ==="
main_count=$(link_skills "$MAIN_WORKSPACE" "$SKILLS_ROOT/shared" "$SKILLS_ROOT/personal" "$BUNDLED_SKILLS")
echo "Linked $main_count skills to $MAIN_WORKSPACE"
ls "$MAIN_WORKSPACE" | sort | sed 's/^/  /'

echo ""
echo "=== Syncing Work Agent (shared + work + bundled) ==="
work_count=$(link_skills "$WORK_WORKSPACE" "$SKILLS_ROOT/shared" "$SKILLS_ROOT/work" "$BUNDLED_SKILLS")
echo "Linked $work_count skills to $WORK_WORKSPACE"
ls "$WORK_WORKSPACE" | sort | sed 's/^/  /'

echo ""
echo "Done."
