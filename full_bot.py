#!/usr/bin/env python3
"""⚡ 红色闪电 - Telegram 消息中转机器人"""
import logging, sqlite3, uuid, httpx
from datetime import datetime, timezone, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from html import escape as _e

T="8721428580:AAFnvVTN_WeI1hJUfV22kfJFmLqFc0BxWb4"
U="HSSGMCBot"
W="TP7VvGHa7YzsMsM2Gqje6DdgGeBcpkkRuh"
P=5
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(message)s")
log=logging.getLogger("bot")

def e(t): return _e(str(t or ""))

def c():
    co=sqlite3.connect("bot.db");co.row_factory=sqlite3.Row;return co

def i():
    d=c()
    d.executescript("""
CREATE TABLE IF NOT EXISTS u(i PRIMARY KEY,n,t DEFAULT 'free',intro DEFAULT '',te,pdx DEFAULT '',sn INTEGER DEFAULT 1,sc INTEGER DEFAULT 1,dnd INTEGER DEFAULT 0,dg INTEGER DEFAULT 0,no INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS g(id INTEGER PRIMARY KEY AUTOINCREMENT,ui,na);
CREATE TABLE IF NOT EXISTS l(i INTEGER PRIMARY KEY AUTOINCREMENT,ui,cc UNIQUE,na,gi DEFAULT 0,uc INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS th(id INTEGER PRIMARY KEY AUTOINCREMENT,oi,si,sn,su,lc,ht DEFAULT '',bl DEFAULT 0,mc DEFAULT 0,hu DEFAULT 0,lt,ct);
CREATE TABLE IF NOT EXISTS m(id INTEGER PRIMARY KEY AUTOINCREMENT,ti,fo DEFAULT 0,ct,ir DEFAULT 0,ca);
""")
    d.commit();d.close();log.info("DB OK")

def gu(i):d=c();r=d.execute("SELECT*FROM u WHERE i=?",(i,)).fetchone();d.close();return dict(r)if r else None
def goc(i,un="",fn=""):
    d=c();r=d.execute("SELECT*FROM u WHERE i=?",(i,)).fetchone()
    if r:d.close();return dict(r)
    te=(datetime.now(timezone.utc)+timedelta(hours=24)).isoformat()
    d.execute("INSERT INTO u(i,n,te)VALUES(?,?,?)",(i,fn,te));d.commit()
    r=d.execute("SELECT*FROM u WHERE i=?",(i,)).fetchone();d.close();return dict(r)
def uu(i,**kw):d=c();d.execute(f"UPDATE u SET {','.join(f'{k}=?'for k in kw)} WHERE i=?",list(kw.values())+[i]);d.commit();d.close()
def tk(i):
    u=gu(i)
    if not u or u.get("t")=="pro":return 1
    te=u.get("te")
    if not te:return 1
    try:return datetime.strptime(te[:19],"%Y-%m-%dT%H:%M:%S")>datetime.now(timezone.utc)
    except:return 1
def tl(i):
    u=gu(i)
    if not u or u.get("t")=="pro":return "无限(VIP)"
    te=u.get("te")
    if not te:return "24小时"
    try:r=datetime.strptime(te[:19],"%Y-%m-%dT%H:%M:%S")-datetime.now(timezone.utc);s=int(r.total_seconds());return f"{s//3600}h{(s%3600)//60}m"if s>0 else"已过期"
    except:return"-"
def ag(ui,na):d=c();d.execute("INSERT INTO g(ui,na)VALUES(?,?)",(ui,na));d.commit();r=d.execute("SELECT*FROM g WHERE id=last_insert_rowid()").fetchone();d.close();return dict(r)
def gg(ui):d=c();rs=d.execute("SELECT*FROM g WHERE ui=?",(ui,)).fetchall();d.close();return[dict(r)for r in rs]
def dg(id_,ui):d=c();d.execute("DELETE FROM g WHERE id=? AND ui=?",(id_,ui));d.execute("UPDATE l SET gi=0 WHERE gi=? AND ui=?",(id_,ui));d.commit();d.close()
def al(ui,na,gi=0):
    cc=uuid.uuid4().hex[:10];d=c();d.execute("INSERT INTO l(ui,cc,na,gi)VALUES(?,?,?,?)",(ui,cc,na,gi));d.commit()
    r=d.execute("SELECT*FROM l WHERE cc=?",(cc,)).fetchone();d.close();return dict(r)
def gl(ui):d=c();rs=d.execute("SELECT*FROM l WHERE ui=? AND gi>=0 ORDER BY i DESC",(ui,)).fetchall();d.close();return[dict(r)for r in rs]
def ggl(ui):
    gs=gg(ui);lks=gl(ui);r=[]
    ug=[l for l in lks if l["gi"]==0]
    if ug:r.append({"gi":0,"na":"未分组","lks":ug})
    for g in gs:
        ml=[l for l in lks if l["gi"]==g["id"]]
        if ml:r.append({"gi":g["id"],"na":g["na"],"lks":ml})
    return r
def glc(cc):d=c();r=d.execute("SELECT*FROM l WHERE cc=?",(cc,)).fetchone();d.close();return dict(r)if r else None
def il(cc):d=c();d.execute("UPDATE l SET uc=uc+1 WHERE cc=?",(cc,));d.commit();d.close()
def dl(id_,ui):d=c();d.execute("UPDATE l SET gi=-1 WHERE i=? AND ui=?",(id_,ui));d.commit();d.close()
def gt(id_):d=c();r=d.execute("SELECT*FROM th WHERE id=?",(id_,)).fetchone();d.close();return dict(r)if r else None
def gct(oi,si,sn,su,cc,ht=""):
    d=c();r=d.execute("SELECT*FROM th WHERE oi=? AND si=?",(oi,si)).fetchone()
    if r:d.execute("UPDATE th SET sn=?,su=? WHERE id=?",(sn,su,r["id"]));d.commit();d.close();return dict(r)
    n=datetime.now().isoformat();d.execute("INSERT INTO th(oi,si,sn,su,lc,ht,ct)VALUES(?,?,?,?,?,?,?)",(oi,si,sn,su,cc,ht,n));d.commit()
    r=d.execute("SELECT*FROM th WHERE id=last_insert_rowid()").fetchone();d.close();return dict(r)
def gts(ui):d=c();rs=d.execute("SELECT*FROM th WHERE oi=? AND bl=0 ORDER BY lt DESC",(ui,)).fetchall();d.close();return[dict(r)for r in rs]
def stb(id_,v):d=c();d.execute("UPDATE th SET bl=? WHERE id=?",(v,id_));d.commit();d.close()
def sm(ti,fo,ct):
    n=datetime.now().isoformat();d=c()
    d.execute("INSERT INTO m(ti,fo,ct,ir,ca)VALUES(?,?,?,?,?)",(ti,1 if fo else 0,ct,1 if fo else 0,n))
    d.execute("UPDATE th SET mc=mc+1,lt=?,hu=CASE WHEN ? THEN hu ELSE 1 END WHERE id=?",(n,fo,ti))
    d.commit();d.close()
def gtm(ti,lm=50):d=c();rs=d.execute("SELECT*FROM m WHERE ti=? ORDER BY ca DESC LIMIT ?",(ti,lm)).fetchall();d.close();return[dict(r)for r in reversed(rs)]
def gmc(ti):d=c();r=d.execute("SELECT COUNT(*)as c FROM m WHERE ti=? AND fo=0 AND ir=0",(ti,)).fetchone();d.close();return r["c"]if r else 0
def mr(ti,oi=None):
    d=c();d.execute("UPDATE m SET ir=1 WHERE ti=? AND fo=0",(ti,))
    if oi:d.execute("UPDATE th SET hu=0 WHERE id=? AND oi=?",(ti,oi))
    d.commit();d.close()
def gua(ui):d=c();r=d.execute("SELECT COUNT(*)as c FROM th WHERE oi=? AND bl=0 AND hu=1",(ui,)).fetchone();d.close();return r["c"]if r else 0
def sts(ui):
    d=c()
    a=d.execute("SELECT COUNT(*)as c FROM th WHERE oi=? AND bl=0",(ui,)).fetchone()["c"]
    tl=d.execute("SELECT COUNT(*)as c FROM m m JOIN th t ON m.ti=t.id WHERE t.oi=?",(ui,)).fetchone()["c"]
    lk=d.execute("SELECT COUNT(*)as c FROM l WHERE ui=? AND gi>=0",(ui,)).fetchone()["c"]
    td=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    td_m=d.execute("SELECT COUNT(*)as c FROM m m JOIN th t ON m.ti=t.id WHERE t.oi=? AND m.ca LIKE ?",(ui,f"{td}%")).fetchone()["c"]
    ua=gua(ui);d.close();return{"a":a,"tl":tl,"lk":lk,"td":td_m,"ua":ua}
def sv(ui,tx=""):d=c();d.execute("UPDATE u SET t='pro',pdx=? WHERE i=?",(tx,ui));d.commit();d.close()
def tu(tx):d=c();r=d.execute("SELECT COUNT(*)as c FROM u WHERE pdx=?",(tx,)).fetchone();d.close();return(r["c"]if r else 0)>0

def mk():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗新建",callback_data="n"),InlineKeyboardButton("📋链接",callback_data="ls"),InlineKeyboardButton("📊统计",callback_data="st")],
        [InlineKeyboardButton("📩消息",callback_data="ib"),InlineKeyboardButton("⚙️设置",callback_data="se"),InlineKeyboardButton("👑VIP",callback_data="vi")],
    ])
def sk():
    u=gu(uid)if'uid'in dir()else None
    def tv(v):return"🟢"if v else"🔴"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{tv(1)}名称",callback_data="tn"),InlineKeyboardButton(f"{tv(1)}渠道",callback_data="tc"),InlineKeyboardButton(f"{tv(1)}免打扰",callback_data="td")],
        [InlineKeyboardButton(f"{tv(1)}日报",callback_data="tg"),InlineKeyboardButton(f"{tv(1)}通知",callback_data="tno"),InlineKeyboardButton("🏠首页",callback_data="ho")],
    ])

def cs(up,ctx):
    u=up.effective_user;ud=goc(u.id,u.username or"",u.first_name or"")
    if ctx.args and ctx.args[0][:3]=="rl_":
        code=ctx.args[0][3:];lk=glc(code)
        if lk:
            owner=gu(lk["ui"])
            if not owner:up.message.reply_text("❌对方已停止使用");return
            if not tk(lk["ui"]):up.message.reply_text("⏰对方免费试用已结束");return
            il(code);s=up.effective_user;th=gct(lk["ui"],s.id,s.first_name or"",s.username or"",code)
            ctx.user_data["ti"]=th["id"];ctx.user_data["oi"]=lk["ui"]
            on=owner.get("n","对方");ln=lk.get("na","")
            msg=f"📬 正在联系 {e(on)}"
            if ln:msg+=f"\n来源渠道：{e(ln)}"
            msg+="\n\n直接发消息即可，对方回复后也会通知你。"
            up.message.reply_text(msg);return
        up.message.reply_text("❌链接无效");return
    ua=gua(u.id)
    if ua>0:up.message.reply_text(f"⚡ 你有 {ua} 条未读消息",reply_markup=mk())
    else:up.message.reply_text(f"👋 欢迎使用红色闪电\n\n/createlink 名称  创建链接\n/link  管理链接\n/inbox  消息列表\n/vip  会员\n/help  帮助",reply_markup=mk())

def cc(up,ctx):
    u=up.effective_user;ud=goc(u.id,u.username or"",u.first_name or"")
    if not tk(ud["i"]):up.message.reply_text("⏰ 试用已结束，/vip 付费后继续使用");return
    nm=" ".join(ctx.args)if ctx.args else"链接"
    lk=al(ud["i"],nm)
    url=f"https://t.me/{U}?start=rl_{lk['cc']}"
    msg=f"✅ {e(nm)}\n\n{url}\n\n无需好友 · 点击链接进入私聊"
    intro=ud.get("intro","")
    if intro:msg+=f"\n——\n{_e(intro)}"
    up.message.reply_text(msg)

def cl(up,ctx):
    u=up.effective_user;ud=goc(u.id,u.username or"",u.first_name or"")
    lks=gl(ud["i"])
    if not lks:up.message.reply_text("🔗 还没有链接，/createlink 名称 创建一个");return
    for l in lks:
        nm=e(l.get("na","未命名"))
        url=f"https://t.me/{U}?start=rl_{l['cc']}"
        tagline="无需好友 · 点击链接进入私聊"
        kb=InlineKeyboardMarkup([[InlineKeyboardButton("📤分享",url=f"https://t.me/share/url?url={url}&text={tagline}")],[InlineKeyboardButton("🗑删除",callback_data=f"dl_{l['i']}")]])
        up.message.reply_text(f"✅ {nm}\n\n{url}\n\n{tagline}",reply_markup=kb)

def ci(up,ctx):
    u=up.effective_user;ud=goc(u.id,u.username or"",u.first_name or"")
    ts=gts(ud["i"])
    if not ts:up.message.reply_text("📩 暂无消息");return
    msg=f"👥 {len(ts)}个联系人 · 点击进入对话\n"
    btns=[]
    for t in ts[:8]:
        n=e(t.get("sn","")or t.get("su","未知"))
        unread=t.get("hu",0)
        badge="🔴"if unread else"✅"
        lt=(t.get("lt","")or"")[11:16]
        last_msgs=gtm(t['id'],1)
        preview=e(last_msgs[0]['ct'][:20])if last_msgs else""
        msg+=f"\n{badge}{n}\n{preview}  {lt}"
        btns.append([InlineKeyboardButton(f"{n}",callback_data=f"chat_{t['id']}")])
    msg+="\n—\n/reply id 回复  ·  /history id 历史"
    up.message.reply_text(msg,reply_markup=InlineKeyboardMarkup(btns))

def cst(up,ctx):
    s=sts(up.effective_user.id)
    up.message.reply_text(f"📊 数据统计\n\n👥 活跃会话：{s['a']}\n📩 未读消息：{s['ua']}\n💬 历史消息：{s['tl']}\n🔗 链接数量：{s['lk']}\n📅 今日消息：{s['td']}")

def cse(up,ctx):
    u=gu(up.effective_user.id)
    if not u:return
    def tv(v):return"🟢"if v else"🔴"
    up.message.reply_html(f"⚙️设置\n{tv(u.get('sn',1))}显示发送者名称\n{tv(u.get('sc',1))}显示来源渠道\n{tv(not u.get('dnd',0))}免打扰模式\n{tv(u.get('dg',0))}每日日报\n{tv(u.get('no',1))}消息通知\n\n点击按钮开关",reply_markup=sk())

def cintro(up,ctx):
    u=gu(up.effective_user.id)
    if not ctx.args:
        cur=u.get("intro","")
        t=f"\n当前：{e(cur)}"if cur else""
        up.message.reply_text(f"📋 个人介绍{t}\n\n/intro 你的介绍");return
    uu(up.effective_user.id,intro=" ".join(ctx.args))
    up.message.reply_text("✅ 已设置")

def ci_clr(up,ctx):uu(up.effective_user.id,intro="");up.message.reply_text("✅已清除")
def cag(up,ctx):
    if not ctx.args:up.message.reply_text("/addgroup 分组名称");return
    g=ag(up.effective_user.id," ".join(ctx.args));up.message.reply_text(f"✅已创建分组 #{g['id']} {e(g['na'])}")
def cgg(up,ctx):
    gs=gg(up.effective_user.id)
    if not gs:up.message.reply_text("暂无分组");return
    up.message.reply_text("\n".join(f"#{g['id']} {e(g['na'])}"for g in gs))
def crg(up,ctx):
    if not ctx.args:up.message.reply_text("/rmgroup 分组ID");return
    try:dg(int(ctx.args[0]),up.effective_user.id);up.message.reply_text("✅已删除")
    except:up.message.reply_text("❌失败")
def cr(up,ctx):
    if not ctx.args or len(ctx.args)<2:up.message.reply_text("/reply 会话ID 回复内容");return
    try:ti=int(ctx.args[0])
    except:up.message.reply_text("❌ID必须是数字");return
    text=" ".join(ctx.args[1:]);th=gt(ti)
    if not th or th["oi"]!=up.effective_user.id:up.message.reply_text("❌会话不存在");return
    sm(ti,True,text);mr(ti,up.effective_user.id)
    try:
        on=th.get("sn","")or"对方"
        ctx.bot.send_message(chat_id=th["si"],text=f"💬 {e(on)} 回复了你\n\n{text}")
        up.message.reply_text(f"✅已回复 {e(th.get('sn','')or th.get('su','用户'))}")
    except:up.message.reply_text("❌发送失败")
def cbk(up,ctx):
    if not ctx.args:up.message.reply_text("/block 会话ID");return
    try:ti=int(ctx.args[0])
    except:up.message.reply_text("❌ID必须是数字");return
    th=gt(ti)
    if not th:up.message.reply_text("❌会话不存在");return
    stb(ti,1);up.message.reply_text(f"🚫已拉黑 {e(th.get('sn','')or th.get('su','用户'))}")
def cub(up,ctx):
    if not ctx.args:up.message.reply_text("/unblock 会话ID");return
    try:ti=int(ctx.args[0])
    except:up.message.reply_text("❌ID必须是数字");return
    th=gt(ti)
    if not th:up.message.reply_text("❌会话不存在");return
    stb(ti,0);up.message.reply_text(f"✅已解除拉黑 {e(th.get('sn','')or th.get('su','用户'))}")
def chist(up,ctx):
    if not ctx.args:up.message.reply_text("/history 会话ID");return
    try:ti=int(ctx.args[0])
    except:up.message.reply_text("❌ID必须是数字");return
    th=gt(ti)
    if not th:up.message.reply_text("❌会话不存在");return
    msgs=gtm(ti,15);n=e(th.get("sn","")or"对方")
    lines=[f"💬 {n}（共{th['mc']}条）\n"]
    for m in reversed(msgs):
        who="我"if m["fo"]else n
        tm=(m["ca"]or"")[11:16]
        lines.append(f"{tm} {who}")
        lines.append(f"{e(m['ct'][:60])}\n")
    up.message.reply_text("\n".join(lines))
    up.message.reply_text("\n".join(lines))
def cblocks(up,ctx):
    ts=gbt(up.effective_user.id)
    if not ts:up.message.reply_text("🚫 黑名单为空");return
    lines=["🚫 已拉黑"]
    for t in ts:lines.append(f"#{t['id']} {e(t.get('sn','')or t.get('su','未知'))}")
    lines.append("\n/unblock id 解除")
    up.message.reply_text("\n".join(lines))
def cv(up,ctx):
    u=gu(up.effective_user.id)
    if u and u.get("t")=="pro":up.message.reply_text("👑 你是VIP");return
    r=tl(up.effective_user.id)
    up.message.reply_text(f"⏰ {r}\n💰 {P} USDT 永久\n\n{W}\n\n/activate TXID")

def ca(up,ctx):
    u=up.effective_user;ud=goc(u.id,u.username or"",u.first_name or"")
    if not ctx.args:
        up.message.reply_text(f"📋 激活VIP\n\n1.转账 {P} USDT (TRC20) 到：\n{W}\n2.复制交易哈希（TXID）\n3.发送 /activate 你的TXID");return
    tx=ctx.args[0].strip()
    if len(tx)<10:up.message.reply_text("❌TXID格式不正确");return
    if tu(tx):up.message.reply_text("❌该TXID已被使用");return
    msg=up.message.reply_text("🔄正在验证链上交易，请稍候...")
    try:
        r=httpx.get(f"https://api.trongrid.io/v1/transactions/{tx}/events",timeout=15)
        if r.status_code!=200:msg.edit_text("❌无法验证，请检查TXID是否正确");return
        ok=False;amt=0
        for ev in r.json().get("data",[]):
            if ev.get("contract_address")!="TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":continue
            if ev.get("event_name")!="Transfer":continue
            res=ev.get("result",{});W="TP7VvGHa7YzsMsM2Gqje6DdgGeBcpkkRuh"
            if res.get("to")!=W:continue
            try:amt=int(res.get("value","0"))
            except:continue
            if amt>=P*10**6:ok=True;break
        if ok:sv(ud["i"],tx);msg.edit_text(f"✅VIP已激活！\n\n金额：{amt/10**6:.1f} USDT\nTXID：{tx[:16]}...\n\n感谢你的支持！所有功能永久可用。")
        else:msg.edit_text("❌未找到有效转账。请确认：\n1.转账到正确地址\n2.金额≥5 USDT\n3.使用TRC20网络")
    except:msg.edit_text("❌验证服务暂时不可用，请稍后再试")

def ch(up,ctx):
    up.message.reply_text(
        "/createlink 名称  创建链接\n"
        "/link  查看链接\n"
        "/inbox  消息\n"
        "/reply id 内容  回复\n"
        "/intro 介绍  设置介绍\n"
        "/addgroup 名称  分组\n"
        "/groups  分组列表\n"
        "/vip  会员\n"
        "/activate TXID  激活\n"
        "/stats  统计\n"
        "/settings  设置\n"
        "/block id  拉黑\n"
        "/unblock id  解除\n"
        "/help  帮助")

def hm(up,ctx):
    # 处理对话模式（点了联系人后直接聊）
    cc=ctx.user_data.get("current_chat")
    if cc:
        th=gt(cc)
        if th:
            txt=up.message.text or""
            sm(cc,True,txt);mr(cc,up.effective_user.id)
            try:
                on=th.get("sn","")or"对方"
                ctx.bot.send_message(chat_id=th["si"],text=txt)
                n=e(th.get("sn","")or"对方")
                up.message.reply_text(f"你  {datetime.now().strftime('%H:%M')}\n{txt}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬继续回复",callback_data=f"chat_{cc}"),InlineKeyboardButton("🔙列表",callback_data="ib")]]))
            except:up.message.reply_text("❌发送失败")
        else:ctx.user_data.pop("current_chat",None)
        return
    # 处理主人回复（点击"回复"按钮后）
    rtid=ctx.user_data.get("reply_thread_id")
    if rtid:
        th=gt(rtid)
        if th:
            txt=up.message.text or""
            sm(rtid,True,txt);mr(rtid,up.effective_user.id)
            try:
                on=th.get("sn","")or"对方"
                ctx.bot.send_message(chat_id=th["si"],text=f"💬 {txt}")
                up.message.reply_text("✅已回复")
            except Exception as ex:log.error(f"回复失败:{ex}");up.message.reply_text("❌发送失败")
        else:ctx.user_data.pop("reply_thread_id",None)
        return
    # 处理发送者发消息（通过链接）
    ti=ctx.user_data.get("ti");oi=ctx.user_data.get("oi")
    if ti and oi:
        th=gt(ti)
        if th:
            if th.get("bl"):up.message.reply_text("🚫对方已将你拉黑");return
            if not tk(oi):up.message.reply_text("⏰对方免费试用已结束");return
            txt=up.message.text or"";sm(ti,False,txt)
            sn=e(th.get("sn","")or th.get("su","用户"))
            if th.get("su"):sn=f"{sn}(@{e(th['su'])})"
            try:
                # 尝试获取发送者头像
                try:
                    photos=ctx.bot.get_user_profile_photos(th["si"],limit=1)
                    if photos and photos.photos:
                        ctx.bot.send_photo(chat_id=oi,photo=photos.photos[0][-1].file_id,caption=f"{sn}\n{txt}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✏️回复",callback_data=f"r_{ti}")]]))
                    else:raise Exception("no photo")
                except:
                    ctx.bot.send_message(chat_id=oi,text=f"📩 {sn}\n{txt}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✏️回复",callback_data=f"r_{ti}")]]))
            except:up.message.reply_text("❌消息发送失败")
            return
    # 默认提示
    up.message.reply_text("📋 使用 /createlink 创建链接，或 /help 查看帮助")

def cbh(up,ctx):
    q=up.callback_query;q.answer();d=q.data;uid=q.from_user.id;ud=goc(uid,up.effective_user.username or"",up.effective_user.first_name or"")
    if d=="ho":
        ua=gua(uid)
        if ua>0:q.edit_message_text(f"⚡欢迎回来！你有 {ua} 条未读消息",reply_markup=mk())
        else:q.edit_message_text("👋欢迎使用红色闪电！/createlink 创建链接",reply_markup=mk())
    elif d=="ls":
        lks=gl(uid)
        if not lks:q.edit_message_text("暂无链接",reply_markup=mk());return
        msgs=[];btns=[]
        for l in lks[:5]:
            url=f"https://t.me/{U}?start=rl_{l['cc']}"
            tagline="无需好友 · 点击链接进入私聊"
            msgs.append(f"✅ {e(l['na'])}\n\n{url}\n\n{tagline}")
            btns.append([InlineKeyboardButton(f"📤分享",url=f"https://t.me/share/url?url={url}&text={tagline}")])
        btns.append([InlineKeyboardButton("🔙返回",callback_data="ho")])
        q.edit_message_text("\n\n".join(msgs),reply_markup=InlineKeyboardMarkup(btns))
    elif d=="st":s=sts(uid);q.edit_message_text(f"📊会话{s['a']}未读{s['ua']}\n💬{s['tl']}🔗{s['lk']}\n📅今日{s['td']}",reply_markup=mk())
    elif d=="ib":
        ts=gts(uid)
        if not ts:q.edit_message_text("暂无消息",reply_markup=mk());return
        msg="👥 联系人"
        for t in ts[:8]:
            n=e(t.get("sn","")or t.get("su","?"))
            b="🔴"if t.get("hu")else""
            lt=(t.get("lt","")or"")[11:16]
            lm=gtm(t['id'],1)
            p=e(lm[0]['ct'][:20])if lm else""
            mc=t['mc'];msg+=f"\n\n{n}({mc})"if b else f"\n\n{n}";msg+=f"\n{p}\n{lt}"
        q.edit_message_text(msg,reply_markup=mk())
    elif d=="se":q.edit_message_text("⚙️设置页面",reply_markup=sk());return
    elif d=="vi":
        u=gu(uid)
        if u and u.get("t")=="pro":q.edit_message_text("👑你是VIP",reply_markup=mk());return
        q.edit_message_text(f"👑VIP {P} USDT永久\n/vip 查看详情",reply_markup=mk())
    elif d=="n":q.edit_message_text("/createlink 名称");return
    elif d.startswith("chat_"):
        ti=int(d.split("_")[1]);th=gt(ti)
        if th:
            ctx.user_data["current_chat"]=ti
            n=e(th.get("sn","")or"对方")
            # 显示最近消息
            msgs=gtm(ti,5);lines=[f"💬 {n}"]
            for m in reversed(msgs):
                who="我"if m["fo"]else n
                tm=(m["ca"]or"")[11:16]
                lines.append(f"\n{tm} {who}\n{e(m['ct'][:40])}")
            mr(ti);#标记已读
            q.edit_message_text("\n".join(lines),reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️回复",callback_data=f"r_{ti}"),InlineKeyboardButton("📋预设",callback_data=f"pr_{ti}")],
                [InlineKeyboardButton("🔙列表",callback_data="ib"),InlineKeyboardButton("🚫拉黑",callback_data=f"b_{ti}")],
            ]))
    elif d.startswith("pr_"):
        ti=int(d.split("_")[1])
        q.edit_message_text("📋 预设回复",reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("好的👌",callback_data=f"sendpr_{ti}_好的，收到")],
            [InlineKeyboardButton("稍后回复⏳",callback_data=f"sendpr_{ti}_稍后回复你")],
            [InlineKeyboardButton("加微信📱",callback_data=f"sendpr_{ti}_方便加个微信吗")],
            [InlineKeyboardButton("🔙返回",callback_data=f"chat_{ti}")],
        ]))
    elif d.startswith("sendpr_"):
        parts=d.split("_",2)
        if len(parts)>=3:
            ti=int(parts[1]);text=parts[2];th=gt(ti)
            if th:
                sm(ti,True,text);mr(ti,uid)
                try:ctx.bot.send_message(chat_id=th["si"],text=f"💬 {text}")
                except:pass
                q.edit_message_text("✅已发送")
    elif d.startswith("r_"):
        ti=int(d.split("_")[1]);th=gt(ti)
        if th:
            ctx.user_data["reply_thread_id"]=ti
            n=e(th.get("sn","")or"对方")
            q.edit_message_text(f"✏️回复 {n}\n\n直接输入内容即可\n或使用 /reply {ti} 内容")
    elif d.startswith("b_"):
        ti=int(d.split("_")[1]);th=gt(ti)
        if th:stb(ti,1);q.edit_message_text(f"🚫已拉黑 {e(th.get('sn','')or'用户')}",reply_markup=mk())
    elif d.startswith("dl_"):
        lid=int(d.split("_")[1]);dl(lid,uid);q.edit_message_text("✅链接已删除",reply_markup=mk())
    elif d.startswith("v_"):
        ti=int(d.split("_")[1]);th=gt(ti)
        if th:
            msgs=gtm(ti,5);lines=[f"📩{e(th.get('sn','')or'会话')}"]
            for m in msgs:lines.append(f"{'你'if m['fo']else'对方'}：{e(m['ct'][:30])}")
            q.edit_message_text("\n".join(lines))
    else:
        tgs={"tn":("sn",1),"tc":("sc",1),"td":("dnd",0),"tg":("dg",0),"tno":("no",1)}
        for k,(key,default)in tgs.items():
            if d==k:
                nv=1-ud.get(key,default);uu(uid,**{key:nv});u2=gu(uid)
                def tv(v):return"🟢"if v else"🔴"
                q.edit_message_text(f"⚙️设置\n{tv(u2.get('sn',1))}显示名称\n{tv(u2.get('sc',1))}显示渠道\n{tv(not u2.get('dnd',0))}免打扰\n{tv(u2.get('dg',0))}日报\n{tv(u2.get('no',1))}通知",reply_markup=sk())
                return

def reg(dp):
    for c,f in[("start",cs),("createlink",cc),("link",cl),("inbox",ci),("messages",ci),("stats",cst),("settings",cse),("intro",cintro),("introclear",ci_clr),("addgroup",cag),("groups",cgg),("rmgroup",crg),("reply",cr),("block",cbk),("unblock",cub),("history",chist),("blocks",cblocks),("vip",cv),("activate",ca),("help",ch)]:
        dp.add_handler(CommandHandler(c,f))
    dp.add_handler(MessageHandler(Filters.text,hm))
    dp.add_handler(CallbackQueryHandler(cbh))
    dp.add_error_handler(lambda u,c:log.error(f"ERR:{c.error}"))

def main():
    i();u=Updater(token=T,use_context=True);reg(u.dispatcher)
    u.start_polling();log.info(f"✅@{U} 运行中");u.idle()
if __name__=="__main__":main()
