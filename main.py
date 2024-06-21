
from docxtpl import DocxTemplate

from daniel import get_context

tpl = DocxTemplate("template.docx")
tpl.render(get_context(tpl))
tpl.save("generated_cv.docx")

print("Successfully generated the CV!")
