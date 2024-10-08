from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.id))
        all_books = result.scalars().all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/<int:id_number>', methods=['GET', 'POST'])
def edit(id_number):
    with app.app_context():
        book = db.session.execute(db.select(Book).where(Book.id == id_number)).scalar()
    if request.method == "POST":
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == id_number)).scalar()
            book_to_update.rating = request.form['rating']
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book, id=id_number)


@app.route('/delete/<int:id_number>')
def delete(id_number):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == id_number)).scalar()
        # or book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
