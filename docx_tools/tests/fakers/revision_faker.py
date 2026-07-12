from faker.providers import BaseProvider

from docx_tools.models.revision import Revision


class RevisionFaker(BaseProvider):

    def generate_revisions(self, number_of_revisions: int = 1):

        revisions: list[Revision] = []

        for i in range(number_of_revisions):
            revisions.append(Revision(
                number=str(i+1),
                date=self.generator.date(),
                description=self.generator.text(max_nb_chars = 40)
            ))
        return revisions