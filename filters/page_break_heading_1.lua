local pagebreak = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
function Header(el)
    if el.level == 1 then
        -- return both the page break and the header as a list
        return { pandoc.RawBlock('openxml', pagebreak), el }
    end
end