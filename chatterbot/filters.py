"""
Filters set the base query that gets passed to the storage adapter.
"""


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, chatterbot, conversation):
        """
        Because this is the base filter class, this method just
        returns the storage adapter's base query. Other filters
        are expected to override this method.
        """
        return chatterbot.storage.base_query


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive responses to prevent
    a chat bot from repeating statements that it has recently said.
    """

    def filter_selection(self, chatterbot, conversation):
        from collections import Counter

        conversation_statements = chatterbot.storage.filter(conversation=conversation)

        text_of_recent_responses = [
            statement.in_response_to for statement in conversation_statements if statement is not None
        ]

        counter = Counter(text_of_recent_responses)

        most_common = counter.most_common(5)

        # Return the query with no changes if there are no statements to exclude
        if not most_common:
            return super(RepetitiveResponseFilter, self).filter_selection(
                chatterbot,
                conversation
            )

        query = chatterbot.storage.base_query.statement_text_not_in(
            most_common
        )

        return query
