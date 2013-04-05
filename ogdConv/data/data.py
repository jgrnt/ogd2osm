class GeneralMixin(object):
        """
        An auxilliary class. Contains the most common methods for all the OSM elements.
        """
        def __init__(self, data):
            if('children' in data):
                self.tags = {item['k']: item['v'] for item in self.filter_children(data, 'tag')}

        @staticmethod
        def filter_children(element, tag_name):
                """
                Extracts from `element` the child elements named `tag_name`, e.g.: self.filter_children(data, 'tag')
                """
                return (i for i in element['children'] if i['name'] == tag_name)

        @property
        def tags_dict(self):
                """
                Converts tags dictionary into dictionaries that represent XML elements.
                """
                return ({'name': 'tag', 'attrs': {'k': k, 'v': v}} for k, v in self.tags.items())

        @property
        def attrs_dict(self):
            return dict()
        
        @property
        def as_dict(self):
                """
                Dumps the whole element into the common dictionary structure (defined in __init__.py).
                """
                return {'name': self.name, 'attrs': self.attrs_dict, 'children': self.tags_dict}

        @staticmethod
        def ref(element):
                """
                Takes the ref attribute from `element` and converts it to integer.
                """
                return int(element['attrs']['ref'])


class ElementMixin(GeneralMixin):
        """
        Element mixin introduces ids: ids are popped from attributes when initialized and added when dumped to a dict. Also ids are used for string representation.
        """
        def __init__(self, data):
                super(ElementMixin, self).__init__(data)
                self.id = int(data['id'])

        def __repr__(self):
                return '%s %s' % (self.__class__.__name__, self.id)

        @property
        def attrs_dict(self):
                d = super(ElementMixin, self).attrs_dict
                d['id'] = self.id
                return d


class Node(ElementMixin):
        """
        OSM Node class
        """
        name = 'node'

        def __init__(self, data):
                super(Node, self).__init__( data)
                self.lat, self.lon = (float(data[x]) for x in  ('lat', 'lon'))  

        @property
        def attrs_dict(self):
                d = super(Node, self).attrs_dict
                d.update({'lon': self.lon, 'lat': self.lat})
                return d


class Way(ElementMixin):
        """
        OSM Way class
        """
        name = 'way'

        def __init__(self,  data):
                super(Way, self).__init__( data)
                self.nodes = [self.doc.nodes[self.ref(nd)] for nd in self.filter_children(data, 'nd')]

        @property
        def as_dict(self):
                data = super(Way, self).as_dict
                data['children'] = chain(
                        data['children'],
                        ({'name': 'nd', 'attrs': {'ref': node.id}} for node in self.nodes),
                )
                return data


class Member(GeneralMixin):
        """
        OSM Relation membership class. Is standalone, since membership also has role to it, which belongs neither to the relation, nor to the member element.
        """
        name = 'member'

        def __init__(self, relation, data):
                self.relation = relation
                self.attrs = data['attrs']
                self.role = self.attrs.pop('role')
                self.member_type = self.attrs.pop('type')
                self.ref = self.ref(data)

        @property
        def tags(self):
                # Relation member elements contain no tags.
                return {}

        @property
        def member(self):
                return self.relation.doc.dicts[self.member_type][self.ref]

        @member.setter
        def member(self, new_member):
                self.ref = new_member.id
                self.member_type = new_member.name

        def __repr__(self):
                return '%s %s in %s as %s' % (self.__class__.__name__, self.member, self.relation, self.role)

        @property
        def attrs_dict(self):
                return {'ref': self.ref, 'type': self.member_type, 'role': self.role}


class Relation(ElementMixin):
        """
        OSM Relation class. Contains Member instances in self.members, which lead to the real relation members (nodes, ways or other relations).
        """
        name = 'relation'

        def __init__(self, doc, data):
                super(Relation, self).__init__(doc, data)
                self.members = [Member(self, i) for i in self.filter_children(data, 'member')]

        @property
        def as_dict(self):
                data = super(Relation, self).as_dict
                data['children'] = chain(
                        data['children'],
                        (m.as_dict for m in self.members),
                )
                return data
