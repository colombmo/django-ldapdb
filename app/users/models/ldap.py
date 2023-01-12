from ldapdb.models.fields import CharField, IntegerField, ListField
import ldapdb.models

class LdapGroup(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = "ou=groups,dc=swice,dc=ch"
    object_classes = ["groupOfNames"]

    # posixGroup attributes
    gid = CharField(db_column="entryUUID", unique=True, max_length=50)
    name = CharField(db_column="cn", max_length=200, primary_key=True)
    members = ListField(db_column="member")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name