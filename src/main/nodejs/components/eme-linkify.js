import linkifyHtml from 'linkifyjs/html'

const label = "ENLACE";
const threshold = 45;
const properties = {
    nl2br: true,
    attributes: href => ({ title: href }),
    format: (value, type) => type === 'url' && value.length > threshold ? label : value
}

export default function linkify (text) {
    return linkifyHtml(text, properties);
}
