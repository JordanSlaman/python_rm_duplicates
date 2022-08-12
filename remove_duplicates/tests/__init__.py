# from .fixtures import test_data_setup
#
# TEST_DIR_PATH = test_data_setup()


# identify_file = tempfile.NamedTemporaryFile(delete=False)



# test_paths = [Path(test_dir_name + test_folder_name) for test_folder_name in test_data.keys()]

# def verify_identify():
#     with open(identify_filename, newline='') as csvfile:
#         identity_reader = csv.reader(csvfile)
#         for row in identity_reader:
#             for file_name in row[1:]:
#                 assert 'dupe' in file_name
#
#     print('Identify test passed!')
#
#
# def verify_remove():
#     for test_folder_path in test_paths:
#         for file_path in test_folder_path.iterdir():
#             assert not 'dupe' in str(file_path)
#
#     print('Remove test passed!')
#
#
# def cleanup_test():
#     test_dir.cleanup()
#     # for test_folder_path in test_paths:
#     #     for file_path in test_folder_path.iterdir():
#     #         file_path.unlink()
#     #     test_folder_path.rmdir()
#     #
#     # base_path = Path(base_pathname)
#     # for file_path in base_path.iterdir():
#     #     file_path.unlink()
#     #
#     # base_path.rmdir()
#
#     print('Test data removed.')
#
#
# if __name__ == '__main__':
#     setup_test()
#
#     identify(
#         [str(p) for p in test_paths],
#         outfile=identify_path,
#         progress=True
#     )
#     verify_identify()
#
#     remove(
#         infile=identify_path,
#         dry_run=False,
#         rm_empty_dirs=False,
#         progress=True
#     )
#     verify_remove()
#
#     cleanup_test()
#
# # TODO: Testing...
# '''
#  - write test for each arg
#  - test for recurse flag
#     if isinstance(dict) in fixture?
#  - verify tempdir & cleanup works
