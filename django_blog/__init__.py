import os
from django.core.management import call_command
from django.test.runner import DiscoverRunner, dependency_ordered
from django.conf import settings

def load_sql(connection, *args, **kwargs):
    if connection.settings_dict["NAME"] != "test_crm_back":
        return
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          "../deploy", "dump.sql"), "r")
    # f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    #                       "../deploy", "database.sql"), "r")

    sql = f.read()
    try:
        cursor = connection.cursor()
        cursor.execute('drop schema public cascade; create schema public;')
        cursor.execute(sql)
        connection.commit()
        # import time
        # st = time.time()
        # print('before load')
        # call_command('loaddata',
        #              os.path.join(os.path.dirname(os.path.realpath(__file__)),
        #                           "fixtures", "initial_data.json"))
        # call_command('loaddata',
        #              os.path.join(os.path.dirname(os.path.realpath(__file__)),
        #                           "fixtures", "order.json"))
        # call_command('loaddata',
        #              os.path.join(os.path.dirname(os.path.realpath(__file__)),
        #                           "fixtures", "sup.json"))
        #
        # # from django.core.management import execute_from_command_line
        # print('after load')
        # print(time.time() - st)
        # execute_from_command_line('loaddata')
    except Exception:
        connection.rollback()
    finally:
        f.close()



class TestImportCustom(DiscoverRunner):

    def setup_test_environment(self, **kwargs):
        settings.AUTHORIZATION_REQUIRED = True
        super(TestImportCustom, self).setup_test_environment(**kwargs)

    def setup_databases(self, **kwargs):
        verbosity, interactive = self.verbosity, self.interactive
        from django.db import connections, DEFAULT_DB_ALIAS

        mirrored_aliases = {}
        test_databases = {}
        dependencies = {}
        default_sig = connections[
            DEFAULT_DB_ALIAS].creation.test_db_signature()
        for alias in connections:
            connection = connections[alias]

            test_settings = connection.settings_dict['TEST']
            if test_settings['MIRROR']:
                mirrored_aliases[alias] = test_settings['MIRROR']
            else:
                item = test_databases.setdefault(
                    connection.creation.test_db_signature(),
                    (connection.settings_dict['NAME'], set())
                )
                item[1].add(alias)

                if 'DEPENDENCIES' in test_settings:
                    dependencies[alias] = test_settings['DEPENDENCIES']
                else:
                    if alias != DEFAULT_DB_ALIAS and connection\
                            .creation.test_db_signature() != default_sig:
                        dependencies[alias] = test_settings.get(
                            'DEPENDENCIES', [DEFAULT_DB_ALIAS])

        # Second pass -- actually create the databases.
        old_names = []
        mirrors = []

        for signature, (db_name, aliases) in dependency_ordered(
                test_databases.items(), dependencies):
            test_db_name = None
            # Actually create the database for the first connection
            for alias in aliases:
                connection = connections[alias]
                if test_db_name is None:
                    try:
                        test_db_name = connection.creation.create_test_db(
                            verbosity,
                            autoclobber=not interactive,
                            serialize=connection.settings_dict.get(
                                "TEST", {}).get("SERIALIZE", True),
                        )
                    except Exception:
                        pass
                    destroy = True
                else:
                    connection.settings_dict['NAME'] = test_db_name
                    destroy = False
                load_sql(connection=connection)
                old_names.append((connection, db_name, destroy))

        for alias, mirror_alias in mirrored_aliases.items():
            mirrors.append((alias, connections[alias].settings_dict['NAME']))
            connections[alias].settings_dict['NAME'] = (
                connections[mirror_alias].settings_dict['NAME'])

        return old_names, mirrors