from data.generators.generator import BaseFakerGenerator

class PasswordGenerator(BaseFakerGenerator):

    def pass_generator(self):
        password = self.faker.password()

        return {
            'new': password,
            'repeat': password
        }

class PasswordPairGenerator(BaseFakerGenerator):

    def generate_password_pair(self, same=True):
        pwd = self.faker.password()
        if same:
            return pwd, pwd
        else:
            return pwd, self.faker.password()
