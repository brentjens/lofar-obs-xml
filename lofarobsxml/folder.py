from lofarobsxml.observationspecificationbase import ObservationSpecificationBase
from lofarobsxml.utilities import lower_case


class Folder(ObservationSpecificationBase):
    r'''
    Translates to a MoM folder. It can contain several children, such
    as other Folders, or Observations. 

    **Parameters**

    name : string
        Name of the folder.

    children : list
        List of items in the folder. These can be Observations or
        Folders.

    description : string
        If provided, sets the description of the MoM folder.

    mom_id : int
        If mom_id is specified, it will add its children to this
        specific MoM folder. If not, a new folder is created in MoM.

    grouping_parent : bool
        Set to True if the folders' children must all share the same
        group ID.

    update_folder : bool
        If True, re-use a folder with the same name if it already
        exists. If it does not, the folder will be created. Do not set
        mom_id when setting update_folder to true.

    **Examples**

    >>> folder = Folder(name     = 'root folder',
    ...                 children =  [Folder(name='child')],
    ...                 description = 'Main folder',
    ...                 mom_id      = 12345,
    ...                 grouping_parent = True)
    >>> print(folder)
    Folder(parent          = NoneType,
           children        = [Folder(parent          = Folder('root folder'),
                                    children        = None,
                                    description     = None,
                                    grouping_parent = False,
                                    initial_status  = 'opened',
                                    mom_id          = None,
                                    name            = 'child',
                                    update_folder   = True)],
           description     = 'Main folder',
           grouping_parent = True,
           initial_status  = 'opened',
           mom_id          = 12345,
           name            = 'root folder',
           update_folder   = True)
    >>> print(folder.xml('test_project'))
    <lofar:folder mom2Id="12345" topology_parent="true">
      <topology>root_folder</topology>
      <name>root folder</name>
      <description>Main folder</description>
      <children>
        <item index="0">
          <lofar:folder topology_parent="false" update_folder="true">
            <topology>root_folder.0.child</topology>
            <name>child</name>
          </lofar:folder>
        </item>
      </children>
    </lofar:folder>
    '''
    def __init__(self, name,
                 children    = None,
                 description = None,
                 mom_id      = None,
                 grouping_parent = False,
                 update_folder = True):
        super(Folder, self).__init__(name, parent=None, children=children)
        self.description     = description
        self.mom_id          = mom_id
        self.grouping_parent = grouping_parent
        self.update_folder   = update_folder


    def xml_prefix(self, project_name):
        preamble = ''
        if self.mom_id:
            preamble = ('<lofar:folder mom2Id="%s" topology_parent="%s">' %
                        (self.mom_id, lower_case(self.grouping_parent)))
        else:
            preamble = ('<lofar:folder topology_parent="%s" update_folder="%s">' %
                        (lower_case(self.grouping_parent), lower_case(self.update_folder)))
        preamble += '\n  <topology>%s</topology>' % self.label()
        preamble += '\n  <name>'+self.name+'</name>'

        if self.description:
            preamble += '\n  <description>'+self.description+'</description>'''
        return preamble

    def xml_suffix(self, project_name):
        return '\n</lofar:folder>'


