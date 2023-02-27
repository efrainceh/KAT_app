from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length
from app import ALLOWED_EXTENSIONS


class KatRunForm(FlaskForm):
    kmer_size = IntegerField('Kmer size', validators=[DataRequired(), NumberRange(min=5, max=1000, message="Size must be between 5 and 1000 bp")])
    run_name = StringField("Run name", validators=[DataRequired(), Length(max=20, message="Run name must be smaller than 20 characters")])
    samples = MultipleFileField("Samples",  validators=[DataRequired()])
    references = MultipleFileField("References",  validators=[DataRequired()])
    submit = SubmitField('Run')

    def validate_samples(self, samples):
        self._validate_files(samples)

    def validate_references(self, references):
        self._validate_files(references)

    def _validate_files(self, files):
        first_file_mimetype = files.data[0].mimetype
        number_of_files = len(files.data)
        if first_file_mimetype == "application/octet-stream":
            raise ValidationError("You must input at least one fasta file")

        if number_of_files > 5:
            raise ValidationError("Maximum number of files is 5")

        for file in files.data:
            extension = file.mimetype.split('/')[-1]
            if extension not in ALLOWED_EXTENSIONS:
                raise ValidationError("Only fasta files are allowed")




