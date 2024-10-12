from decimal import Decimal
from enum import Enum
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from wtforms import (
    Form,
    StringField,
    SelectField,
    DecimalRangeField,
)
from wtforms.widgets import RangeInput
from wtforms.validators import(
    DataRequired,
    AnyOf,
    EqualTo,
)


app = Flask(__name__)

class Opinion(Enum):
    VERY_GOOD="VERY GOOD"
    GOOD="GOOD"
    BAD="BAD"
    VERY_BAD="VERY BAD"


class Quiz(Form):
    name: str = StringField(validators=[DataRequired("WHERE ARE NAME??HUH??")])
    choice: str = SelectField(
        choices=Opinion.__members__,
        validators=[DataRequired(), AnyOf(Opinion.__members__)],
    )
    rating: Decimal = DecimalRangeField(
        widget=RangeInput(step=Decimal("1")),
        validators=[
            EqualTo("rating_confirm"),
        ],
        )
    rating_confirm: Decimal = DecimalRangeField(
        widget=RangeInput(step=Decimal("1")),
    )
    
    def save(self):
        print(f"name: {self.name}; choice: {self.choice}; rating: {self.rating}")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/create")
def get_opinion():
    form = Quiz()
    return render_template("form.html", form=form)


@app.post("/create")
def quiz_create():
    form = Quiz(
        request.form,
    )

    if form.validate():
        form.save()
        return redirect(url_for(index.__name__))
    elif form.errors:
        print(f"{form.errors=}")
        print(f"{form.form_errors=}")
        for _, error in form.errors.items():
            flash(error)
    return render_template("form.html", form=form)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()