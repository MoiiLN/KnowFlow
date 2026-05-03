# KnowFlow Backend Setup - TODO

## Plan Progress ✅ COMPLETE\n- [x] User approved plan\n- [x] Step 1: Install uv ✅ uv 0.11.8\n- [x] Step 2: Sync uv dependencies ✅ .venv created (37 packages incl. Django 6.0.2)\n- [x] Step 3: Run migrations ✅ All applied\n- [x] Step 4: Superuser created ✅ admin/admin@example.com

## Commands to run (in order from /home/dpl_moises/knowflow)

1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Reload shell**: `source ~/.bashrc` (or restart terminal)
3. **Sync deps**: `uv sync`
4. **Migrate** (cd Backend && just migrate): `cd Backend && just migrate`
5. **Create superuser**: `cd Backend && just create-su`
6. **Run dev**: `cd Backend && just dev 8000`

