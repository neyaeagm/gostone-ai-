from flask import Flask, request, jsonify
import uuid
import time

app = Flask(__name__)

# =====================
# Geçici veritabanı (demo)
# =====================
users = {}
approved_users = set()

# =====================
# Kullanıcı kayıt
# =====================
@app.route("/register", methods=["POST"])
def register():
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "created_at": time.time(),
        "credits": 50,
        "subscription": "trial",
        "approved": False
    }
    return jsonify({
        "user_id": user_id,
        "trial_days": 15,
        "credits": 50
    })

# =====================
# Yetkili onayı (AI-3)
# =====================
@app.route("/approve_user", methods=["POST"])
def approve_user():
    admin_key = request.headers.get("X-ADMIN-KEY")
    user_id = request.json.get("user_id")

    if admin_key != "SECRET_ADMIN_KEY":
        return jsonify({"error": "Yetkisiz"}), 403

    if user_id in users:
        users[user_id]["approved"] = True
        approved_users.add(user_id)
        return jsonify({"status": "Kullanıcı onaylandı"})

    return jsonify({"error": "Kullanıcı bulunamadı"}), 404

# =====================
# AI-1 (herkes)
# =====================
@app.route("/ai1", methods=["POST"])
def ai1():
    return jsonify({"response": "AI-1 çalışıyor"})

# =====================
# AI-2 (aboneler)
# =====================
@app.route("/ai2", methods=["POST"])
def ai2():
    user_id = request.headers.get("X-USER-ID")
    if user_id not in users:
        return jsonify({"error": "Kullanıcı yok"}), 404
    return jsonify({"response": "AI-2 çalışıyor"})

# =====================
# AI-3 (sadece yetkili onaylı)
# =====================
@app.route("/ai3", methods=["POST"])
def ai3():
    user_id = request.headers.get("X-USER-ID")
    if user_id not in approved_users:
        return jsonify({"error": "Yetkili onayı gerekli"}), 403
    return jsonify({"response": "AI-3 aktif (gelişmiş)"})

if __name__ == "__main__":
    app.run(debug=True)
