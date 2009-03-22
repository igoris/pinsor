"""Responsible for retrieving components from the object graph"""
from pinsor.ioc.exceptions import NotFoundInObjectGraphError

class ComponentModelRetrieval(object):
    """used for searching object graph to retrieve component models"""
    
    def get_component_model(self, graph, key, clsout):
        """attempts to find one and only one component based 
        on class type, then filtering down to key"""
        matchingnodes = []
        for node in graph.iteritems():
            if node[1].classtype is clsout:
                matchingnodes.append(node)
        if len(matchingnodes) is 1:
            return matchingnodes[0][1]
        if len(matchingnodes) > 1:
            for matchednode in matchingnodes:
                if matchednode[0] == key:
                    return matchednode[1]
            raise NotFoundInObjectGraphError("matching classes found of type "\
             + str(clsout) + " but key of " + key + " not found")
        raise NotFoundInObjectGraphError("no matching classes found of type "\
         + str(clsout))
        