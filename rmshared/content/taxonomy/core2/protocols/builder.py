from rmshared.content.taxonomy import protocols

interface_to_factory_map = {
    protocols.IFilters: protocols.Builder.Factory(lambda labels_, ranges_: Filters().add_protocol().add_protocol()..., (protocols.ILabels, protocols.IRanges)),
    protocols.IOrders: protocols.Builder.Factory(Orders, (protocols.IFields,)),
    protocols.ILabels: protocols.Builder.Factory(Labels, (protocols.IFields, protocols.IValues)),
    protocols.IRanges: protocols.Builder.Factory(Ranges, (protocols.IFields, protocols.IValues)),
    protocols.IFields: protocols.Builder.Factory(Fields, ()),
    protocols.IValues: protocols.Builder.Factory(Values, ()),
}
