from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # کلید امنیتی

# صفحه اصلی (صفحه ثبت‌نام)
@app.route('/')
def home():
    return render_template('register.html')

# مسیر ثبت‌نام - دریافت اطلاعات و ذخیره در دیتابیس
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # اتصال به دیتابیس
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # بررسی اینکه آیا کاربر قبلاً وجود دارد
    c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    existing_user = c.fetchone()

    # اگر کاربر قبلاً ثبت‌نام کرده باشد
    if existing_user:
        flash('Username or email already exists!', 'error')
        conn.close()
        return redirect(url_for('home'))

    # هش کردن پسورد
    hashed_password = generate_password_hash(password)

    # ذخیره اطلاعات کاربر جدید
    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    conn.commit()
    conn.close()


    flash('Registration successful!', 'success')
    return redirect(url_for('welcome'))  # هدایت به صفحه خوش‌آمدگویی



# مسیر صفحه خوش‌آمدگویی
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # اتصال به دیتابیس و بررسی یوزر
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[3], password):
            session['username'] = user[1]  # user[1] = username
            session['email'] = user[2]     # user[2] = email
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        # اگر اعتبارسنجی موفق بود:
        session['username'] = username
        session['email'] = email
        return redirect(url_for('profile'))
    return render_template('login.html')
    return "If this email exists, a reset link has been sent."
    return render_template('forgot_password.html')  # حتما اسم فایل HTML همینه؟
@app.route('/profile')



def profile():
    if 'username' in session:
        return render_template('profile.html', username=session.get('username'), email=session.get('email'))
    else:
        return redirect(url_for('login'))    


@app.route('/logout')
def logout():
    session.clear()  # یا session.pop('username', None) برای حذف تنها اطلاعات خاص
    return redirect(url_for('login'))  # هدایت به صفحه لاگین

# ساخت دیتابیس و جدول‌ها اگر وجود نداشته باشند


if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, 
                                                 username TEXT, 
                                                 email TEXT, 
                                                 password TEXT)''')
    conn.commit()  # ذخیره تغییرات در دیتابیس
    conn.close()
    
    # اجرای اپلیکیشن
    app.run(debug=True, port=5001)
