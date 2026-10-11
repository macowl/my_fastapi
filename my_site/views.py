from pydantic import BaseModel
from fastapi import  Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from db import get_db
from .models import *

from sqlalchemy.orm import Session
from datetime import datetime

class VisitBody(BaseModel):
    page: str   # 页面路径，如 /home、/about、/product/123


router = APIRouter()

@router.post("/api/visit")
def record_visit(
    body: VisitBody,
    request: Request,
    db: Session = Depends(get_db),
):
    """前端每次加载页面时调用这个接口，自动计数+1"""
    page = body.page
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_ip = request.client.host if request.client else "unknown"

    # ========== 页面维度统计 ==========
    page_stat = db.query(PageStat).filter(PageStat.page_path == page).first()

    if page_stat is None:
        # 新页面，插入记录
        page_stat = PageStat(
            page_path=page,
            total=1,
            today=1,
            last_date=today,
            last_visit=now,
            last_ip=client_ip,
        )
        db.add(page_stat)
        page_total = 1
        page_today = 1
    else:
        # 已有页面，更新数据
        page_stat.total += 1
        page_total = page_stat.total

        if page_stat.last_date == today:
            page_stat.today += 1
        else:
            page_stat.today = 1
        page_today = page_stat.today

        page_stat.last_date = today
        page_stat.last_visit = now
        page_stat.last_ip = client_ip

    # ========== 全局维度统计 ==========
    site_stat = db.query(SiteStat).filter(SiteStat.id == 1).first()

    if site_stat is None:
        site_stat = SiteStat(id=1, total=1, today=1, last_date=today)
        db.add(site_stat)
        site_total = 1
        site_today = 1
    else:
        site_stat.total += 1
        site_total = site_stat.total

        if site_stat.last_date == today:
            site_stat.today += 1
        else:
            site_stat.today = 1
        site_today = site_stat.today

        site_stat.last_date = today

    db.commit()

    return {
        "page_total": page_total,
        "page_today": page_today,
        "site_total": site_total,
        "site_today": site_today,
    }


@router.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """查看所有页面的访问统计"""
    site = db.query(SiteStat).filter(SiteStat.id == 1).first()
    pages = db.query(PageStat).order_by(PageStat.total.desc()).all()

    return {
        "total": site.total if site else 0,
        "today": site.today if site else 0,
        "pages": [
            {
                "page_path": p.page_path,
                "total": p.total,
                "today": p.today,
                "last_visit": p.last_visit,
                "last_ip": p.last_ip,
            }
            for p in pages
        ],
    }


@router.get("/api/stats/{page_path:path}")
def get_page_stats(page_path: str, db: Session = Depends(get_db)):
    """查看单个页面的访问统计"""
    page = "/" + page_path
    page_stat = db.query(PageStat).filter(PageStat.page_path == page).first()

    if page_stat is None:
        return {"error": "页面不存在"}

    return {
        "page_path": page_stat.page_path,
        "total": page_stat.total,
        "today": page_stat.today,
        "last_visit": page_stat.last_visit,
        "last_ip": page_stat.last_ip,
    }


@router.get("/", response_class=HTMLResponse)
def home(db: Session = Depends(get_db)):
    """简单的展示页面，看所有页面访问量"""
    site = db.query(SiteStat).filter(SiteStat.id == 1).first()
    pages = db.query(PageStat).order_by(PageStat.total.desc()).all()

    rows = ""
    for p in pages:
        rows += f"""
        <tr>
            <td>{p.page_path}</td>
            <td>{p.total}</td>
            <td>{p.today}</td>
            <td>{p.last_visit}</td>
            <td>{p.last_ip}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>访问统计</title>
        <style>
            body {{ font-family: sans-serif; max-width: 900px; margin: 50px auto; }}
            h1 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 30px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f5f5f5; }}
            .summary {{ text-align: center; margin: 20px 0; }}
            .number {{ font-size: 32px; color: #333; }}
        </style>
    </head>
    <body>
        <h1>📊 网站访问统计</h1>
        <div class="summary">
            <span class="number">{site.total if site else 0}</span> 总访问 &nbsp;|&nbsp;
            <span class="number">{site.today if site else 0}</span> 今日访问
        </div>
        <table>
            <tr>
                <th>页面路径</th>
                <th>总访问</th>
                <th>今日访问</th>
                <th>最后访问时间</th>
                <th>最后访问IP</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html
