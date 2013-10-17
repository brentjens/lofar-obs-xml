r'''
A base class for classes that generate (part of) the xml needed to
enter information into MoM.
'''

def indent(self, string, amount):
    r'''
    Indent a multi-line string by the given amount.
    
    string : string
        The string to indent.
    
    amount : int
        The direction and amount to indent.

    **Examples**

    >> indent('Hi\nThere', 2)
      Hi
      There

    >> indent('Hi\nThere\n\n', -1)
    i
    here
    <BLANKLINE>
    <BLANKLINE>
    '''
    lines = string.split('\n')
    if amount > 0:
        lines = [' '*amount + line for line in lines]
    if amount < 0:
        lines = [line[-amount:] for line in lines]
    return '\n'.join(lines)
    




class ObservationSpecificationBase(object):
    r'''
    A base class from which to derive instances which can generate
    specifications for observations and pipelines in formats that MoM,
    the XML Generator by Alwin de Jong, or users can read.
    
    **Parameters**
    
    name : string
        A free form string labelling the instance.
    
    parent : ObservationSpecificationBase instance
        The parent of the curent instance. 

    children : None or a list of ObservationSpecificationBase
        The children of the current instance.

    **Examples**

    >>> OSB = ObservationSpecificationBase
    '''
    
    def __init__(self, name, parent, children = None):
        self.name     = name
        self.parent   = parent
        self.children = children


    def __repr__(self):
        name    = self.__class__.__name__
        as_dict = self.__dict__
        members = as_dict.keys()
        longest_member = sorted([len(s) for s in members])[-1]
        
        member_strings = [mem.ljust(longest_member)+' = '+repr(as_dict[mem])
                          for mem in members
                          if mem != 'parent']
        member_strings += ['parent'.ljust(longest_member) + ' = ' +
                           self.parent.__class__.__name__+
                           '('+str(self.parent.name)+')']
        sep = '\n'+' '*(len(name)+1)
        indented_member_strings = [('\n'+ ' '*(longest_member+3)).join(
            member.split('\n'))
                                   for member in member_strings]
        unadjusted =  ',\n'.join(indented_member_strings)
        return name+'('+sep.join(unadjusted.split('\n'))+')'




    def xml_prefix(self, project_name):
        r'''
        Generate the XML content that goes before the child list.
        Should return a string. This is one of the two virtual
        methods. The other one is ``xml_suffix()``.
        '''
        raise NotImplementedError(
            '%s.xml_prefix(self, project_name) not implemented' %
            self.__class__.__name__)


        
    def xml_suffix(self, project_name):
        r'''
        Generate the XML content that goes after the child
        list. Should return a string. This is one of the two virtual
        methods. The other one is ``xml_prefix()``.
        '''
        raise NotImplementedError(
            '%s.xml_suffix(self, project_name) not implemented' %
            self.__class__.__name__)



    def xml(self, project_name):
        r'''
        Actually generate the required XML. This method calls two
        other methods, which may be overridden: xml_prefix() and
        xml_suffix().
        '''
        xml_string = self.xml_prefix(project_name)
        if self.children:
            childlist_format ='\n<children>%s\n</children>'
            child_format     = '\n<item index="%d">\n%s\n</item>'
            children = [child_format % (index, child.xml(project_name))
                        for index, child in enumerate(self.children)]
            xml_string += childlist_format % '\n'.join(children)
        xml_string += self.xml_prefix(project_name)
        return indent(xml_string, 2*self.tree_depth())
        



    def label(self):
        r'''
        Returns an ascii label that reflects the full path of the
        current instance in the observation set specification.
        '''
        if self.parent:
            str_format = '%s.%d.%s' 
            return str_format % (self.parent.label(),
                                 self.parent.child_id(self),
                                 str(self.name))
        return str(self.name)


        
    def child_id(self, instance):
        r'''
        Return the child ID of object ``instance`` if it is in 
        ``self.children``

        **Parameters**
        
        instance : ObservationSpecificationBase
            The instance for which one wants the position in the
            ``self.children`` list.
        '''
        if self.children is None or len(self.children) == 0:
            raise ValueError(
                'ObservationSpecificationBase{%s}.child_id(): %r is not in list' % 
                (self.__class__.__name__, instance))
        return [id[child] for child in self.children].index(instance)



    def append_child(self, instance):
        r'''
        Append a child to ``self.children``. This method also calls
        set_parent() on the the child, to ensure that the parent is
        set correctly.

        **Parameters**
        
        instance : ObservationSpecificationBase
            The object to add to self.children.
        '''
        if self.children is None:
            self.children = []
        self.children.append(instance)
        return instance.set_parent(self)
        
        

    def set_parent(self, instance):
        r'''
        Set self.parent to ``instance``.
        
        **Parameters**
        
        instance : ObservationSpecificationBase
            The instance of the parent node.
        '''
        self.parent = instance
        return instance



    def tree_depth(self):
        r'''
        Return the depth of the current node in the tree. A node
        without parent is automatically at depth 0.
        '''
        if self.parent is None:
            return 0
        else:
            return self.parent.tree_depth() + 1



        
            
        
