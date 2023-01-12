from ldapdb.models.fields import CharField, IntegerField, ListField, PasswordField
import ldapdb.models

# Class for representing an LDAP group entry.
class LdapGroup(ldapdb.models.Model):
    # LDAP meta-data
    base_dn = "ou=groups,dc=swice,dc=ch"
    object_classes = ["groupOfNames"]

    # posixGroup attributes
    #gid = CharField(db_column="entryUUID", unique=True, max_length=50, default = unique_random_string)
    name = CharField(db_column="cn", max_length=200, primary_key=True)
    members = ListField(db_column="member")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Class for representing an LDAP person
class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = "ou=users,dc=swice,dc=ch"
    object_classes = ["person", "organizationalPerson", "inetOrgPerson"]

    # person attributes
    sn = CharField(db_column="sn", unique=True, max_length=200)
    cn = CharField(db_column="cn", max_length=200, primary_key=True)
    uid = CharField(db_column="uid", unique=True, max_length=200)
    email = CharField(db_column="mail", unique=True, max_length=200)
    first_name = CharField(db_column="displayName", max_length=200, null=True)
    last_name = CharField(db_column="givenName", max_length=200, null=True)
    password = PasswordField()
    

    def __str__(self):
        return self.sn

    def __unicode__(self):
        return self.sn