all:
	pdflatex main.tex

twice:
	pdflatex main.tex
	pdflatex main.tex

full:
	pdflatex main.tex
	bibtex main.aux
	pdflatex main.tex
	pdflatex main.tex
