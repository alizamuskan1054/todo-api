# Todo API — Practice Project (Testing + Docker + CI/CD)

Chota Django + DRF Todo API taake yeh 4 cheezein practice ho sakein:
1. Test cases likhna
2. Docker mein containerize karna
3. GitHub Actions se CI/CD pipeline
4. DevOps ka basic flow samajhna

---

## 1. Local run (bina Docker)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API: `http://127.0.0.1:8000/api/todos/`

---

## 2. Tests kaise likhte/chalate hain

File: `todos/tests.py`

- `APITestCase` (DRF) use hoti hai — Django ke normal `TestCase` ka hi extension hai, bas API responses check karna easy banati hai.
- `setUp()` — har test se pehle chalta hai, fresh test data banata hai.
- Har method jo `test_` se start ho, wo automatically ek test case hai.
- `self.client.get/post/patch/delete()` — asli HTTP request nahi jaati, Django test client fake request simulate karta hai (fast + isolated).
- Test database alag hoti hai (memory mein), asli data kabhi touch nahi hota.

Chalane ka command:
```bash
python manage.py test todos -v 2
```

Types of tests jo yahan cover hain:
| Test | Kya check karta hai |
|---|---|
| `test_list_todos` | GET list sahi data de raha hai |
| `test_create_todo` | POST se naya record banta hai |
| `test_create_todo_missing_title_fails` | Bad input par 400 error |
| `test_retrieve_single_todo` | Ek specific record GET ho raha hai |
| `test_update_todo` | PATCH se field update ho rahi hai |
| `test_delete_todo` | DELETE se record hat raha hai |
| `test_retrieve_nonexistent_todo_returns_404` | Galat id par 404 |

---

## 3. Docker

**Docker kya hai?** Aapke app + uske dependencies (Python version, libraries) ek "container" (isolated box) mein pack ho jate hain, taake "mere system pe to chal raha tha" wala problem na ho — jahan bhi Docker chale, app waise hi chalega.

Build aur run:
```bash
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

`Dockerfile` line-by-line samjho (comments file mein bhi hain):
- `FROM python:3.12-slim` → base image (chota Linux + Python)
- `WORKDIR /app` → container ke andar working folder
- `COPY requirements.txt .` + `RUN pip install` → dependencies pehle install (caching ke liye)
- `COPY . .` → baaki code copy
- `CMD [...]` → container start hote hi migrate + gunicorn server chalao

---

## 4. DevOps + CI/CD — concept

**DevOps** = Development + Operations ko milakar kaam karne ka tareeqa, taake code likhna → test karna → deploy karna sab automated aur fast ho, manual galtiyan kam hon.

**CI (Continuous Integration)**: Jab bhi code push/PR ho, automatically:
- Dependencies install hon
- Tests chalein
- Agar test fail → developer ko turant pata chal jaye (deploy hi nahi hoga galat code)

**CD (Continuous Delivery/Deployment)**: Agar tests pass ho jayein, to automatically:
- Docker image build ho
- (Optional) Docker Hub/registry par push ho
- Server par deploy ho jaye

**Kahan use hota hai?** Har real-world company (aapki School ERP jaisi) mein — jab teammates (Aliza, Namrah) ka code merge hota hai, CI pipeline automatically check karti hai ke naya code purane feature ko break to nahi kar raha, phir deploy hota hai — bina kisi ke manually server pe jaake commands chalaye.

### Pipeline file: `.github/workflows/ci.yml`

- `on: push/pull_request` → trigger kab chalega
- `jobs: test` → pehle tests chalte hain
- `jobs: build` → `needs: test` likha hai matlab yeh job tabhi chalega jab test job **pass** ho
- Real deployment ke liye Docker Hub push + server SSH/deploy step add hota hai (file mein example comment kiya hua hai)

**GitHub par kaise dekhein**: repo push karne ke baad **"Actions"** tab mein jaake pipeline run live dekh sakti ho — kaunsa step chal raha hai, pass/fail kya hua.

---

## Practice checklist

- [ ] Isko apne GitHub repo mein push karo
- [ ] "Actions" tab mein CI pipeline run hote dekho
- [ ] Ek naya test khud likho (e.g. `test_completed_filter`)
- [ ] Ek test jaan-boojh kar fail karo, dekho pipeline red ho jati hai
- [ ] Dockerfile mein koi cheez badlo (e.g. env var), rebuild karo
