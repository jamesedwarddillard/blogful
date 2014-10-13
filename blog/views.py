import mistune
from flask import render_template, request, redirect, url_for

from blog import app
from database import session
from models import Post

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
	# Zero indexed page
	page_index = page - 1

	count = session.query(Post).count()

	start = page_index * paginate_by
	end = start + paginate_by

	total_pages = (count - 1) / paginate_by + 1
	has_next = page_index < total_pages - 1
	has_prev = page_index > 0

	posts = session.query(Post)
	posts = posts.order_by(Post.datetime.desc())
	posts = posts[start:end]

	return render_template("posts.html",
		posts=posts, 
		has_next=has_next,
		has_prev=has_prev,
		page=page,
		total_pages=total_pages
	)

@app.route("/post/<int:post_id>")
def view_post(post_id):
	#Zero indexed posts
	post_index = post_id - 1

	posts = session.query(Post)
	count = session.query(Post).count()

	if post_id < 1 or post_id > count:
		return render_template("not_found.html")
	else: 
		selected_post = posts[post_index]
		return render_template("post_view.html", post = selected_post,)


@app.route("/post/add", methods=["GET"])
def add_post_get():
	return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
def add_post_post():
	post = Post(
		title = request.form["title"],
		content=mistune.markdown(request.form["content"]),
	)
	session.add(post)
	session.commit()
	return redirect(url_for("posts"))

@app.route("/post/<int:post_id>/edit", methods = ["GET"])
def edit_post_get(post_id):
	#Zero indexed posts
	post_index = post_id - 1

	posts = session.query(Post)
	count = session.query(Post).count()

	if post_id < 1 or post_id > count:
		return render_template("not_found.html")
	else: 
		selected_post = posts[post_index]
		return render_template("edit_post.html", post = selected_post,)

@app.route("/post/<int:post_id>/edit", methods = ["POST"])
def edit_post_post(post_id):
	post = session.query(Post).filter_by(id = post_id).first()
	post.title = request.form["title"]
	post.content = mistune.markdown(request.form["content"])
	session.commit()
	return redirect(url_for("posts"))


@app.route("/post/<int:post_id>/delete", methods = ["GET"])
def delete_post_get(post_id):
	post = session.query(Post).filter_by(id = post_id).first()
	return render_template("delete_post.html", post = post)

@app.route("/post/<int:post_id>/delete", methods = ["POST"])
def delete_post_post(post_id):
	post = session.query(Post).filter_by(id = post_id).first()
	session.delete(post)
	session.commit()
	return redirect(url_for("posts"))


